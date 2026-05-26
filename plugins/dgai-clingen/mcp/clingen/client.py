"""HTTP client for ClinGen's public CSpec Registry API.

CSpec exposes JSON for ClinGen affiliations (VCEPs/GCEPs) and their linked
genes. Docs: https://cspec.genome.network/cspec/ui/svi/help

No auth is required for read-only access. We keep the surface area small —
two queries and a normalizer — so the MCP tools stay thin.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any, Iterable

import httpx

DEFAULT_BASE_URL = "https://cspec.genome.network/cspec"
DEFAULT_TIMEOUT = 5.0  # seconds, end-to-end. Acceptance target is < 5s.
USER_AGENT = "dgai-clingen/0.1 (+https://github.com/deepgene/deepgene-plugins)"

# Affiliation IDs are five-digit numerics. VCEPs start with 5, GCEPs with 4,
# Working Groups with 1. See clinicalgenome.org/affiliation/.
_AFFIL_ID_RE = re.compile(r"^\d{5}$")
# Gene symbols are HGNC short symbols, e.g. "OTC", "BRCA1", "TP53". Accept
# 1-15 chars of letters/digits/hyphens, no spaces.
_GENE_SYMBOL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9\-]{0,14}$")


class ClinGenError(RuntimeError):
    """Raised for unrecoverable CSpec errors (network, 5xx, malformed JSON)."""


class ClinGenNotFound(LookupError):
    """Raised when CSpec returns no entity for the requested identifier."""


log = logging.getLogger("clingen.client")


@dataclass(frozen=True)
class IdentifierKind:
    kind: str  # "affiliation_id" | "gene_symbol"
    value: str


def classify_identifier(raw: str) -> IdentifierKind:
    """Decide whether the caller handed us a 5-digit panel ID or a gene symbol.

    Five-digit numeric strings are always treated as affiliation IDs even if
    they happen to be a gene name elsewhere — ClinGen's affiliation IDs
    never collide with HGNC gene symbols.
    """
    if raw is None:
        raise ValueError("identifier is required")
    s = str(raw).strip()
    if not s:
        raise ValueError("identifier is empty after stripping whitespace")
    if _AFFIL_ID_RE.match(s):
        return IdentifierKind("affiliation_id", s)
    if _GENE_SYMBOL_RE.match(s):
        return IdentifierKind("gene_symbol", s.upper())
    raise ValueError(
        f"identifier {raw!r} is neither a 5-digit affiliation ID nor a valid "
        "HGNC-style gene symbol"
    )


class ClinGenClient:
    """Thin httpx wrapper around the CSpec REST endpoints we need.

    Construct one per process and reuse it — httpx clients pool connections,
    so calling twice is much cheaper than instantiating twice.
    """

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        # We accept an injected client so tests can swap in respx/vcr layers
        # without us having to special-case anything.
        self._client = client or httpx.Client(
            timeout=timeout,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            follow_redirects=True,
        )

    # ---- low-level ---------------------------------------------------------

    def _get_json(self, path: str, params: dict[str, str] | None = None) -> Any:
        url = f"{self.base_url}{path}"
        try:
            resp = self._client.get(url, params=params)
        except httpx.HTTPError as exc:
            raise ClinGenError(f"network error calling {url}: {exc}") from exc

        if resp.status_code == 404:
            raise ClinGenNotFound(f"CSpec returned 404 for {url}")
        if resp.status_code >= 500:
            raise ClinGenError(
                f"CSpec returned {resp.status_code} for {url}: {resp.text[:200]}"
            )
        if resp.status_code >= 400:
            # 4xx other than 404 typically means a malformed identifier.
            raise ClinGenNotFound(
                f"CSpec returned {resp.status_code} for {url}: {resp.text[:200]}"
            )

        try:
            return resp.json()
        except ValueError as exc:
            raise ClinGenError(f"CSpec returned non-JSON for {url}: {exc}") from exc

    # ---- public ------------------------------------------------------------

    def fetch_affiliation(self, affiliation_id: str) -> dict:
        """Return the CSpec entity for one affiliation, detail=high.

        Uses the non-specific /id/{val} endpoint. The type-specific path
        /Affiliation/id/{val} began returning 400 "INVALID URL" when the
        CSpec API was updated (confirmed 2026-05-26). The generic endpoint
        returns the same entity and entContent shape, but now wrapped in the
        new {"data": {"Organization": [entity]}} envelope — _unwrap_entity
        strips it.
        """
        raw = self._get_json(f"/id/{affiliation_id}", params={"detail": "high"})
        return _unwrap_entity(raw)

    def fetch_gene_links(self, gene_symbol: str) -> dict:
        """Return a synthetic entity with ldFor.Affiliation for the gene's panels.

        CSpec changed in early 2026: /Gene/id/{symbol}/ldFor now returns
        SequenceVariantInterpretation spec entities instead of a Gene entity
        with an ldFor.Affiliation block. We fetch each spec's detail to find
        its parent Organization and rebuild the shape normalize_gene_panel_links
        expects: {"ldFor": [{"Affiliation": [org, ...]}]}.
        """
        raw = self._get_json(f"/Gene/id/{gene_symbol}/ldFor", params={"detail": "high"})
        specs = (raw.get("data") or {}).get("SequenceVariantInterpretation") or []

        affiliations: list[dict] = []
        for spec in specs:
            ldhId = spec.get("ldhId")
            if not ldhId:
                continue
            try:
                spec_raw = self._get_json(
                    f"/SequenceVariantInterpretation/id/{ldhId}",
                    params={"detail": "high"},
                )
                spec_entity = _unwrap_entity(spec_raw)
                for org in (spec_entity.get("ldFor") or {}).get("Organization") or []:
                    affiliations.append(org)
            except (ClinGenError, ClinGenNotFound):
                continue

        return {"ldFor": [{"Affiliation": affiliations}]}

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "ClinGenClient":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


# ---- response unwrapper -----------------------------------------------------


def _unwrap_entity(raw: dict) -> dict:
    """Strip the CSpec API envelope that appeared in early 2026.

    Two new shapes:
      list-wrapped:  {"data": {"TypeName": [entity, ...]}, ...}
      direct:        {"data": {entity fields...}, ...}

    Falls through to returning raw unchanged if neither pattern matches
    (handles old shape and injected test objects).
    """
    data = raw.get("data")
    if not isinstance(data, dict):
        return raw
    for val in data.values():
        if isinstance(val, list) and val and isinstance(val[0], dict):
            return val[0]
    if "entId" in data or "entContent" in data or "ldFor" in data:
        return data
    return raw


# ---- response normalizers ---------------------------------------------------
#
# CSpec wraps everything in {entId, entType, entContent: {...}, ld: [...]}.
# These helpers crack open the wrapper and project just what the MCP tools
# need to return, so the tool surface stays stable even if CSpec adds fields.


def normalize_panel(entity: dict) -> dict:
    """Project a CSpec Affiliation entity to a stable shape for MCP callers."""
    content = entity.get("entContent") or {}
    return {
        "panel_id": entity.get("entId") or content.get("affiliation_id"),
        "name": content.get("affiliation_fullname")
        or content.get("name")
        or entity.get("entId"),
        "kind": _infer_panel_kind(entity.get("entId"), content),
        "status": content.get("approval_status") or content.get("status"),
        "scope": content.get("scope") or content.get("description"),
        "url": (
            f"https://clinicalgenome.org/affiliation/{entity.get('entId')}/"
            if entity.get("entId")
            else None
        ),
        "cspec_url": entity.get("ldhIri") or entity.get("entIri"),
        "source": "cspec.genome.network",
    }


def normalize_gene_panel_links(entity: dict) -> list[dict]:
    """From a Gene entity's ldFor block, list affiliations referencing the gene.

    CSpec wraps each ldFor entry as a dict whose key is the entity type, e.g.
    ``{"Affiliation": [{...}, ...]}`` — but the type name may vary across API
    versions. We accept any entry whose value is a list and looks like an
    affiliation (5-digit entId or affiliation_fullname in entContent).
    """
    out: list[dict] = []
    seen: set[str] = set()

    def _maybe_add(affil: dict) -> None:
        content = affil.get("entContent") or {}
        ent_id = affil.get("entId") or content.get("affiliation_id")
        if ent_id is None:
            return
        ent_id = str(ent_id)  # entId is sometimes an int in ldFor responses
        if not ent_id or ent_id in seen:
            return
        # Filter to affiliation-shaped entities: 5-digit numeric IDs only.
        if not (ent_id.isdigit() and len(ent_id) == 5):
            return
        seen.add(ent_id)
        out.append(
            {
                "panel_id": ent_id,
                "name": content.get("affiliation_fullname")
                or content.get("name")
                or ent_id,
                "kind": _infer_panel_kind(ent_id, content),
                "url": f"https://clinicalgenome.org/affiliation/{ent_id}/",
            }
        )

    for block in entity.get("ldFor") or []:
        if not isinstance(block, dict):
            continue
        # Try the historically correct "Affiliation" key first, then fall back
        # to scanning all values in case the key name changed.
        affil_list = block.get("Affiliation") or []
        if not affil_list:
            # Scan every key whose value is a list of dicts.
            for val in block.values():
                if isinstance(val, list):
                    affil_list = val
                    break
        for affil in affil_list or []:
            if isinstance(affil, dict):
                _maybe_add(affil)
    return out


def extract_chairs(entity: dict) -> list[dict]:
    """Pull chair-role members out of a CSpec Affiliation entity.

    CSpec sometimes carries `members` or `coordinators` arrays inside
    `entContent`. We pick anything with a `role` containing 'chair'
    (case-insensitive). If nothing matches we fall back to entries flagged
    as `is_chair`/`is_coordinator` truthy, then to the `approver` list as a
    last resort. We return a structured list so the MCP caller can render
    or filter; the empty list is a valid result when CSpec has nothing.
    """
    content = entity.get("entContent") or {}
    chairs: list[dict] = []

    def _add(person: dict, role_hint: str) -> None:
        chairs.append(
            {
                "name": person.get("name")
                or person.get("fullname")
                or _join_first_last(person),
                "role": person.get("role") or role_hint,
                "affiliation": person.get("affiliation")
                or person.get("institution"),
                "email": person.get("email"),
            }
        )

    members: Iterable[dict] = _coerce_people(content.get("members"))
    for m in members:
        role = (m.get("role") or "").lower()
        if "chair" in role:
            _add(m, m.get("role") or "Chair")

    if not chairs:
        for m in _coerce_people(content.get("coordinators")):
            _add(m, m.get("role") or "Coordinator")

    if not chairs:
        approvers = content.get("approver") or content.get("approvers") or []
        if isinstance(approvers, list):
            for entry in approvers:
                if isinstance(entry, str):
                    chairs.append(
                        {"name": entry, "role": "Approver", "affiliation": None, "email": None}
                    )
                elif isinstance(entry, dict):
                    _add(entry, entry.get("role") or "Approver")

    # Drop entries with no name at all — those are useless.
    return [c for c in chairs if c.get("name")]


# ---- internals --------------------------------------------------------------


def _infer_panel_kind(ent_id: str | None, content: dict) -> str | None:
    explicit = (content.get("type") or content.get("kind") or "").upper()
    if explicit in {"VCEP", "GCEP"}:
        return explicit
    if not ent_id:
        return None
    # ClinGen convention: 5xxxx = VCEP, 4xxxx = GCEP, 1xxxx = Working Group.
    first = ent_id[:1]
    return {"5": "VCEP", "4": "GCEP", "1": "Working Group"}.get(first)


def _coerce_people(value: Any) -> list[dict]:
    if not value:
        return []
    if isinstance(value, list):
        return [v for v in value if isinstance(v, dict)]
    if isinstance(value, dict):
        return [value]
    return []


def _join_first_last(person: dict) -> str | None:
    first = person.get("first_name") or person.get("firstName")
    last = person.get("last_name") or person.get("lastName")
    parts = [p for p in (first, last) if p]
    return " ".join(parts) if parts else None
