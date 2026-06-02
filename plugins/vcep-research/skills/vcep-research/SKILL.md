---
name: vcep-research
description: Produce a one-page, fully-cited research briefing on a ClinGen Variant or Gene Curation Expert Panel (VCEP/GCEP) or a single gene. Trigger this skill whenever the user wants to research a ClinGen panel or a gene's curation status before outreach, a Gene Report, or a call; asks "what's the status of the X panel / who chairs it / what's the recent ClinVar activity"; or needs a structured briefing covering panel status, chair and coordinator, scope, recent ClinVar activity, and three to five linked references. The skill is data-first: it resolves the panel through the dgai-clingen MCP, pulls recent ClinVar activity and literature from NCBI, and returns a Markdown briefing where every claim is footnoted to a source URL. It is generic logic, no DeepGene context baked in; data-source query recipes and the output template live in context/.
---

# VCEP Research

## What this skill does

Given a gene symbol or a ClinGen affiliation ID, this skill produces a one-page Markdown briefing on the relevant Curation Expert Panel. The briefing covers panel status, the chair and coordinator, panel scope, recent ClinVar activity, and three to five recent linked references. Every factual line carries a footnote to the source it came from. A briefing with an unsourced claim is not finished.

This is the logic-only skill. It defines what a VCEP research briefing *is* and the procedure for building one from public data. The exact query recipes (ClinGen MCP, PubMed and ClinVar E-utilities, OMIM) live in `context/data-sources.md`. The output skeleton lives in `context/briefing-template.md`. No DeepGene-specific content belongs in this skill; a project layer can wrap it later if a specific framing is needed.

## When to use this skill versus another path

Use this skill when:

- Researching a ClinGen panel or a gene's curation posture before outreach, a call, or a Gene Report
- You need panel status, the roster, scope, and recent ClinVar/literature signal in one structured place
- Every claim needs to be traceable to a public source

Use a different path when:

- You are researching a **person** (a coordinator's background, publications, role) for an outreach email. That is the `recipient-research` procedure in the `outreach` plugin, not this skill.
- You need a **practitioner-level disease and protocol cover document** for a Gene Report. That is the `gene-brief` skill (T3.7), which goes deeper on disease biology, evidence-code challenges, and open questions. This skill is the upstream research pass, not the cover doc.

## Dependencies

- **Required: the `dgai-clingen` MCP** (plugin `dgai-clingen`). This skill calls its `lookup_panel` and `list_chairs` tools for panel metadata and the roster. If the `clingen` MCP server is not connected, stop and tell the user to install/enable `dgai-clingen@dgai-plugins` first.
- **Preferred: the `pubmed-database` skill** (K-Dense, if installed) for the literature step. It wraps NCBI E-utilities with MeSH terms and Boolean operators. If it is not installed, fall back to calling NCBI E-utilities directly via the recipes in `context/data-sources.md`. Either path is acceptable; prefer `pubmed-database` when present.
- **Optional: an OMIM API key** (`OMIM_API_KEY` env var) for the phenotype line. Without it, cite the OMIM entry page and GeneReviews instead. The briefing is still valid without OMIM.

## Inputs needed before starting

- A gene symbol (e.g. `OTC`, `ASS1`) **or** a 5-digit ClinGen affiliation ID (e.g. `50100`).
- If the user gives a gene that maps to more than one panel, ask which panel they mean, or briefly list the candidates and proceed with the most relevant one.

If the input is ambiguous (a disease name, a panel name in prose), resolve it to a gene symbol or affiliation ID first, then proceed.

## Procedure

Run these steps in order. Capture the source URL for every fact as you go; you will need them for the footnotes. The full query recipes are in `context/data-sources.md`.

1. **Resolve the panel.** Call `lookup_panel(gene_or_panel)` from the ClinGen MCP. Read the "Known data limitations" in `context/data-sources.md` first — the two query paths return different, partial shapes:
   - **Gene symbol** (e.g. `OTC`): use this for the real panel **name** (the CSpec spec title) and the gene→panel association. Do not trust the returned `panel_id`/`url`/`kind` on this path; the ID is a CSpec spec entity, not the five-digit affiliation ID.
   - **Five-digit affiliation ID** (e.g. `50100`): use this for `kind` (VCEP/GCEP), the IDs, and `cspec_url`. Note that `name`, `status`, and `scope` come back null on this path.

   If the query was a gene symbol and multiple panels come back, pick the variant-curation panel; note the others. If `ok` is false or `not_found`, continue with what other sources provide (a gene can have literature and ClinVar activity without a usable CSpec entry).

2. **Get the roster.** `list_chairs` needs a five-digit affiliation ID and currently returns an empty roster for known panels (see the limitations note). So: if you only have a gene symbol, you cannot reach the roster through the MCP today — get the chair and coordinator from the **ClinGen affiliation page** (`https://clinicalgenome.org/affiliation/<id>/`) and footnote that page. Call `list_chairs(panel_id)` when you do have the affiliation ID and it returns names; capture name, role, and institution. If the roster is empty either way, say "no chair listed in CSpec; see the ClinGen affiliation page" plainly. Do not invent names.

3. **Characterize recent ClinVar activity.** Query ClinVar for the gene (recipe in `context/data-sources.md`): total submitted variants, count modified in the last two years, the breakdown by clinical significance, and any recent reclassifications or notable review-status changes. Capture the ClinVar gene-view URL for the footnote. This is the signal that distinguishes an active panel from a dormant one.

4. **Pull three to five recent references.** Prefer the `pubmed-database` skill; otherwise run the PubMed E-utilities query in `context/data-sources.md` (gene + variant-curation terms, sorted by date, last ~3 years). For each kept reference capture the PMID, title, first/last author, year, and the `https://pubmed.ncbi.nlm.nih.gov/PMID/` link. Keep the three to five that bear on variant classification for this gene; drop the rest. One line each on why it matters.

5. **Add the phenotype line (OMIM).** One sentence on the disease and inheritance tied to the panel scope, sourced from OMIM (API if `OMIM_API_KEY` is set, otherwise the OMIM entry page) or GeneReviews. Keep it to a line; the full disease overview is the `gene-brief` skill's job, not this one.

6. **Infer panel stage and synthesize.** CSpec `status` comes back null today, so lean the stage inference on the ClinVar activity from step 3 (and `status` only if a future MCP build populates it). Classify the panel stage (active curation, protocol development, recruiting, dormant, or unknown) using the taxonomy in `context/briefing-template.md`. For `scope`, since the MCP returns null, pull it from the published CSpec spec doc (`cspec_url`) or the ClinGen affiliation page. Then assemble the briefing per the template. Mark any field you could not fill as `unknown` rather than guessing.

## Output format

Follow `context/briefing-template.md` exactly. The briefing is one page of Markdown with these sections: header (gene/panel, ID, kind, ClinGen link), panel status and stage, chairs and coordinator, scope and phenotype, recent ClinVar activity, key literature (three to five linked references), and a References footnote section. Apply the repo `style-guide.md` to the prose before returning.

## Citation discipline (mandatory)

Every factual line carries a Markdown footnote (`[^1]`, `[^2]`, …) pointing to the source it came from: ClinGen/CSpec facts to the panel or CSpec URL, ClinVar facts to the ClinVar gene-view URL, each reference to its PubMed URL, the phenotype line to OMIM or GeneReviews. The References section at the bottom lists every footnote with its full URL. If a claim cannot be linked to a source, remove the claim. Do not return a briefing with an unsourced fact.

## When data is missing

- **No CSpec entry for the panel** (`not_found`): build the briefing from ClinVar and literature; note that ClinGen has no published criteria specification yet, which usually means the panel is recruiting or pre-protocol.
- **Null `status`/`scope` from the affiliation path** (the current MCP behavior): get scope from the CSpec spec doc (`cspec_url`) or the ClinGen affiliation page; if neither resolves it, mark scope `unknown`. Do not leave a status claim unsourced.
- **Empty roster from `list_chairs`**: state "no chair listed in CSpec" and link the ClinGen affiliation page so the user can check the SPA directly.
- **Sparse or no recent literature**: report the low count as a real signal (a quiet gene), do not pad with off-topic papers.
- **No OMIM key**: cite the OMIM entry page and/or GeneReviews; do not block on it.
