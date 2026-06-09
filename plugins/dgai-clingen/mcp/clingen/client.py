"""HTTP client for ClinGen's public CSpec Registry API.

CSpec exposes JSON for ClinGen affiliations (VCEPs/GCEPs) and their linked
genes. Docs: https://cspec.genome.network/cspec/ui/svi/help

No auth is required for read-only access. We keep the surface area small —
two queries and a normalizer — so the MCP tools stay thin.
"""
from __future__ import annotations

import csv
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import httpx

# Bundled snapshot of the ClinGen leadership directory.
# Source: vcep-directory/clingen_leadership_contacts.csv (refresh periodically).
DATA_DIR = Path(__file__).parent.parent.parent / "data"
_PANEL_INDEX_CACHE: dict[str, str] | None = None  # panel_id -> panel_name
_ROSTER_CACHE: list[dict] | None = None           # parsed CSV rows

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

        Uses the non-specific /id/ endpoint — CSpec retired /Affiliation/id/
        as of early 2026. The response is wrapped:
            {"data": {"<Type>": [entity, ...]}}
        so we unwrap before returning.
        """
        raw = self._get_json(
            f"/id/{affiliation_id}",
            params={"detail": "high"},
        )
        return _unwrap_entity(raw)

    def fetch_gene_links(self, gene_symbol: str) -> dict:
        """Return the CSpec /ldFor response for a gene.

        detail=high is required — med omits entContent, which carries the
        tagNameSpaces affiliation IDs we need to resolve panels.
        """
        return self._get_json(
            f"/Gene/id/{gene_symbol}/ldFor",
            params={"detail": "high"},
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "ClinGenClient":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


# ---- response normalizers ---------------------------------------------------
#
# CSpec wraps everything in {entId, entType, entContent: {...}, ld: [...]}.
# These helpers crack open the wrapper and project just what the MCP tools
# need to return, so the tool surface stays stable even if CSpec adds fields.



def _unwrap_entity(raw) -> dict:
    """Unwrap CSpec's early-2026 response envelope.

    /id/{val} now returns: {"data": {"<Type>": [entity, ...]}}
    For backward compat we also pass through bare entity dicts.
    """
    if isinstance(raw, dict):
        data = raw.get("data")
        if isinstance(data, dict):
            for entities in data.values():
                if isinstance(entities, list) and entities:
                    return entities[0]
        # Bare entity (old format or direct /{type}/id/ endpoint)
        if "entId" in raw or "entType" in raw or "ldhId" in raw:
            return raw
    raise ClinGenError(f"unexpected CSpec response shape: {str(raw)[:200]}")


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


def normalize_gene_panel_links(raw: dict) -> list[dict]:
    """From a CSpec /Gene/id/{symbol}/ldFor response, list linked panels.

    The endpoint returns {"data": {"SequenceVariantInterpretation": [svi, ...]}}.
    Each SVI carries the affiliation ID in entContent.tagNameSpaces[0] (with
    explicit entContent.affiliation_id checked first for forward compat).
    """
    out: list[dict] = []
    seen: set = set()

    def _maybe_add(ent_id, name, content):
        sid = str(ent_id) if ent_id is not None else None
        if not sid or sid in seen:
            return
        seen.add(sid)
        out.append({
            "panel_id": sid,
            "name": name or sid,
            "kind": _infer_panel_kind(sid, content),
            "url": f"https://clinicalgenome.org/affiliation/{sid}/",
        })

    data = raw.get("data") if isinstance(raw, dict) else None

    # Current format (2026+): data.SequenceVariantInterpretation
    for svi in (data or {}).get("SequenceVariantInterpretation") or []:
        content = svi.get("entContent") or {}
        tags = content.get("tagNameSpaces") or []
        affil_id = (
            content.get("affiliation_id")
            or content.get("affiliation")
            or (tags[0] if tags else None)
        )
        if affil_id:
            _maybe_add(
                affil_id,
                content.get("affiliation_fullname")
                or content.get("affiliation_name")
                or content.get("title")
                or content.get("shortTitle"),
                content,
            )
        else:
            log.debug("SVI without affiliation identifier: %s", svi.get("entId"))

    # Legacy format: data.Affiliation (pre-2026 ldFor responses)
    for affil in (data or {}).get("Affiliation") or []:
        content = affil.get("entContent") or {}
        _maybe_add(
            affil.get("entId"),
            content.get("affiliation_fullname") or content.get("name"),
            content,
        )

    # Oldest format: bare entity with ldFor blocks (cassette compat)
    for block in (raw.get("ldFor") if isinstance(raw, dict) else None) or []:
        for affil in block.get("Affiliation", []) or []:
            content = affil.get("entContent") or {}
            _maybe_add(
                affil.get("entId"),
                content.get("affiliation_fullname") or content.get("name"),
                content,
            )

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


# ---- local directory fallback -----------------------------------------------
#
# CSpec currently returns an empty roster for most panels. We fall back to a
# bundled snapshot of clingen_leadership_contacts.csv (from vcep-directory).


def _load_panel_index() -> dict[str, str]:
    """Return a {panel_id: panel_name} dict from the bundled panel index JSON."""
    global _PANEL_INDEX_CACHE
    if _PANEL_INDEX_CACHE is not None:
        return _PANEL_INDEX_CACHE
    path = DATA_DIR / "clingen_panel_index.json"
    if not path.exists():
        log.warning("panel index not found at %s", path)
        _PANEL_INDEX_CACHE = {}
        return _PANEL_INDEX_CACHE
    import json
    data = json.loads(path.read_text(encoding="utf-8"))
    _PANEL_INDEX_CACHE = {row["panel_id"]: row["name"] for row in data if "panel_id" in row}
    return _PANEL_INDEX_CACHE


def _load_roster_csv() -> list[dict]:
    """Return all rows from the bundled leadership contacts CSV."""
    global _ROSTER_CACHE
    if _ROSTER_CACHE is not None:
        return _ROSTER_CACHE
    path = DATA_DIR / "clingen_leadership_contacts.csv"
    if not path.exists():
        log.warning("leadership contacts CSV not found at %s", path)
        _ROSTER_CACHE = []
        return _ROSTER_CACHE
    with path.open(encoding="utf-8", newline="") as fh:
        _ROSTER_CACHE = list(csv.DictReader(fh))
    return _ROSTER_CACHE


def get_local_roster(panel_id: str) -> list[dict]:
    """Return chairs and coordinators for a panel from the local CSV snapshot.

    Looks up the panel name by ID, then filters the leadership CSV for rows
    where all_panels_and_roles contains that panel name with role Chairs or
    Coordinators. Returns a list in the same shape as extract_chairs().
    """
    index = _load_panel_index()
    panel_name = index.get(panel_id)
    if not panel_name:
        log.debug("panel_id %s not found in local panel index", panel_id)
        return []

    rows = _load_roster_csv()
    results: list[dict] = []
    for row in rows:
        panels_and_roles = row.get("all_panels_and_roles", "")
        # Match e.g. "Urea Cycle Disorders Variant Curation Expert Panel (Chairs)"
        for target_role in ("Chairs", "Coordinators"):
            marker = f"{panel_name} ({target_role})"
            if marker in panels_and_roles:
                results.append({
                    "name": row.get("person_name", "").strip(),
                    "role": target_role.rstrip("s"),  # "Chair" / "Coordinator"
                    "affiliation": row.get("institution", "").strip() or None,
                    "email": (
                        row.get("clingen_email", "").strip()
                        or row.get("orcid_emails", "").strip()
                        or None
                    ),
                    "source": "local_directory",
                })
                break  # one role per person per panel

    log.debug("local roster for %s (%s): %d entries", panel_name, panel_id, len(results))
    return results


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
