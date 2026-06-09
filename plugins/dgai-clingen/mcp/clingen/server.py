"""dgai-clingen MCP server.

Two tools, both backed by ClinGen's public CSpec Registry:

    lookup_panel(gene_or_panel)  → panel metadata for a gene symbol or
                                   5-digit affiliation ID.
    list_chairs(panel_id)        → chair-role members for an affiliation.

Run directly (`python -m clingen.server`) for stdio MCP transport. The plugin
manifest at .claude-plugin/plugin.json wires Claude Code to invoke this exact
entrypoint.
"""
from __future__ import annotations

import logging
import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from .client import (
    ClinGenClient,
    ClinGenError,
    ClinGenNotFound,
    _load_panel_index,
    classify_identifier,
    extract_chairs,
    get_local_roster,
    normalize_gene_panel_links,
    normalize_panel,
)

logging.basicConfig(
    level=os.environ.get("DGAI_CLINGEN_LOG_LEVEL", "INFO"),
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
log = logging.getLogger("clingen.server")


mcp = FastMCP("clingen")

# Lazy module-level client. We keep one per process so connection pooling
# kicks in across calls.
_client: ClinGenClient | None = None


def _panel_from_index(panel_id: str) -> dict[str, Any]:
    """Return minimal panel metadata from the local panel index."""
    name = _load_panel_index().get(panel_id, "")
    return {"panel_id": panel_id, "name": name, "source": "local_directory"}


def _get_client() -> ClinGenClient:
    global _client
    if _client is None:
        _client = ClinGenClient()
    return _client


@mcp.tool(
    name="lookup_panel",
    description=(
        "Look up a ClinGen Variant or Gene Curation Expert Panel by a HGNC "
        "gene symbol (e.g. 'OTC', 'BRCA1') or a 5-digit affiliation ID "
        "(e.g. '50013'). Returns panel metadata: name, kind (VCEP/GCEP), "
        "scope, ClinGen URL, and the CSpec entity URL. When called with a "
        "gene symbol, returns every affiliation whose CSpec specification "
        "references that gene."
    ),
)
def lookup_panel(gene_or_panel: str) -> dict[str, Any]:
    """Resolve a gene symbol or affiliation ID to ClinGen panel metadata."""
    try:
        ident = classify_identifier(gene_or_panel)
    except ValueError as exc:
        return {"ok": False, "error": str(exc), "query": gene_or_panel}

    client = _get_client()

    try:
        if ident.kind == "affiliation_id":
            entity = client.fetch_affiliation(ident.value)
            return {
                "ok": True,
                "query": ident.value,
                "query_kind": "affiliation_id",
                "panels": [normalize_panel(entity)],
            }
        # gene_symbol
        entity = client.fetch_gene_links(ident.value)
        panels = normalize_gene_panel_links(entity)
        return {
            "ok": True,
            "query": ident.value,
            "query_kind": "gene_symbol",
            "panels": panels,
        }
    except ClinGenNotFound as exc:
        return {
            "ok": False,
            "error": "not_found",
            "detail": str(exc),
            "query": ident.value,
            "query_kind": ident.kind,
        }
    except ClinGenError as exc:
        log.exception("CSpec call failed")
        return {
            "ok": False,
            "error": "upstream_error",
            "detail": str(exc),
            "query": ident.value,
            "query_kind": ident.kind,
        }


@mcp.tool(
    name="list_chairs",
    description=(
        "List chair-role members for a ClinGen affiliation by its 5-digit "
        "panel ID (e.g. '50013'). Returns name, role, institutional "
        "affiliation, and (when CSpec exposes it) email. If CSpec has no "
        "chairs for the panel, falls back to coordinators then approvers."
    ),
)
def list_chairs(panel_id: str) -> dict[str, Any]:
    """Return the chair roster for the affiliation behind `panel_id`."""
    try:
        ident = classify_identifier(panel_id)
    except ValueError as exc:
        return {"ok": False, "error": str(exc), "panel_id": panel_id}

    if ident.kind != "affiliation_id":
        return {
            "ok": False,
            "error": "panel_id must be a 5-digit ClinGen affiliation ID",
            "panel_id": panel_id,
        }

    client = _get_client()
    entity = None
    try:
        entity = client.fetch_affiliation(ident.value)
    except (ClinGenNotFound, ClinGenError) as exc:
        log.warning("CSpec unavailable for panel %s: %s — trying local fallback", ident.value, exc)

    chairs = extract_chairs(entity) if entity else []
    roster_source = "cspec" if (entity and chairs) else "unknown"
    if not chairs:
        chairs = get_local_roster(ident.value)
        if chairs:
            roster_source = "local_directory"
            log.debug("used local directory fallback for panel %s", ident.value)

    panel_meta = normalize_panel(entity) if entity else _panel_from_index(ident.value)
    return {
        "ok": True,
        "panel_id": ident.value,
        "panel": panel_meta,
        "chairs": chairs,
        "chair_count": len(chairs),
        "roster_source": roster_source,
    }


def main() -> None:
    """Run the MCP server over stdio. Claude Code launches us this way."""
    mcp.run()


if __name__ == "__main__":
    main()
