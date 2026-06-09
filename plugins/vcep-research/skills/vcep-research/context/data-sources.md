# Data-source recipes for VCEP research

Exact queries for each source the `vcep-research` skill pulls from. These are generic: no DeepGene context here. Capture the URL listed under "Footnote link" for every fact so the briefing's citations resolve.

## 1. ClinGen panel metadata (dgai-clingen MCP)

Tools from the `dgai-clingen` plugin (MCP server `clingen`):

- `lookup_panel(gene_or_panel)` — accepts an HGNC gene symbol (`OTC`, `ASS1`) or a 5-digit affiliation ID (`50100`). Returns:
  ```
  { ok, query, query_kind, panels: [
      { panel_id, name, kind, status, scope, url, cspec_url, source } ] }
  ```
- `list_chairs(panel_id)` — accepts a 5-digit affiliation ID. Returns:
  ```
  { ok, panel_id, panel: {...}, chairs: [
      { name, role, affiliation, email? } ], chair_count }
  ```

Notes:
- A gene symbol can return several panels (every affiliation whose CSpec spec references that gene). Pick the variant-curation panel for the gene; note the others.
- `list_chairs` falls back to coordinators, then approvers, when CSpec has no explicit chair role. The `role` field tells you which you got.
- **Footnote link:** the `url` field (`https://clinicalgenome.org/affiliation/<id>/`) for panel facts; `cspec_url` when citing the raw specification.

### Local directory fallback (added 2026-06-09)

When `list_chairs` returns `chair_count: 0` (the current CSpec behavior for most panels), the MCP now automatically falls back to a bundled snapshot at `plugins/dgai-clingen/data/clingen_leadership_contacts.csv`. The snapshot is sourced from the `vcep-directory` repo. Refresh it by copying a fresh export from `vcep-directory/clingen_leadership_contacts.csv` when the data goes stale. The `roster_source` field in the response tells you which path was used (`"cspec"` vs `"local_directory"`).

### Known data limitations (verified live 2026-06-02)

The current `dgai-clingen` MCP returns less than the briefing ideally wants. Plan around these until the MCP gap is closed (tracked against dgai-clingen / #23):

- **The gene path returns the CSpec *specification* entity, not the affiliation.** `lookup_panel("OTC")` returns `panel_id: "156"` and `lookup_panel("TP53")` returns `"009"` — three-digit spec IDs, not the five-digit affiliation IDs `list_chairs` needs (OTC's affiliation is 50100; TP53's is 50013). The `url` it builds (`/affiliation/156/`) is therefore wrong on the gene path, and `kind` is unreliable (`null` or `"Working Group"`). What the gene path *is* good for: the real panel **name** (the spec title) and the gene→panel association.
- **No gene→affiliation bridge.** From a gene symbol the MCP does not give you the five-digit affiliation ID, so you cannot chain `lookup_panel(gene)` → `list_chairs(panel_id)` today. Pass a five-digit affiliation ID directly when you need the roster, or resolve it from the ClinGen affiliation page.
- **The affiliation path returns null `name`, `status`, and `scope`.** `lookup_panel("50100")` gives `kind: "VCEP"`, the IDs, and `cspec_url`, but `name` is the bare ID and `status`/`scope` are `null`. Get scope and status from the published CSpec specification doc (`cspec_url`) or the ClinGen affiliation page instead.
- **`list_chairs` returns roster data from the local directory fallback** when CSpec returns 400/404 (current behavior for all affiliation ID lookups). Check `roster_source` in the response — `"local_directory"` means the bundled CSV was used. Footnote the ClinGen affiliation page (`panel.url`) for roster facts, not the CSpec URL.

Net effect: from the MCP you can reliably get `kind`, the IDs/URLs, `cspec_url`, the roster (via local fallback), and (gene path) the panel name. Status and scope still come from the ClinGen affiliation page or CSpec spec doc.

## 2. PubMed literature (NCBI E-utilities)

Prefer the `pubmed-database` skill when installed. Otherwise call E-utilities directly.

**Search (esearch):**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=20&sort=date&datetype=pdat&reldate=1095&term=<TERM>
```
- `reldate=1095` limits to roughly the last three years; drop it to widen.
- Append `&api_key=<NCBI_API_KEY>` if one is set (raises the rate limit from 3 to 10 requests/sec).

**Term construction** for a gene's variant-curation literature:
```
<GENE>[Title/Abstract] AND (variant classification[Title/Abstract] OR pathogenicity[Title/Abstract] OR ACMG[Title/Abstract] OR "sequence variant"[Title/Abstract] OR reclassification[Title/Abstract])
```
Add `OR <PANEL NAME>[Title/Abstract]` if the panel has a recognizable name.

**Summaries (esummary):** feed the returned PMIDs back:
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=<PMID1,PMID2,...>
```
This gives title, authors, source, and pubdate without fetching full records.

- **Footnote link:** `https://pubmed.ncbi.nlm.nih.gov/<PMID>/`

## 3. ClinVar recent activity (NCBI E-utilities)

**Total variants for the gene (esearch, count only):**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&retmode=json&retmax=0&term=<GENE>[gene]
```
Read `esearchresult.count` for the total.

**Recently modified variants (last two years):**
```
...&term=<GENE>[gene]&datetype=mdat&reldate=730
```
The drop in count between this and the total characterizes how active the gene is now.

**Significance / review status:** pull a page of summaries to break down by clinical significance and review status (star rating):
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&retmode=json&retmax=50&id=<IDs from esearch>
```
Look at `germline_classification`, `review_status`, and `last_evaluated` on each record. Note recent reclassifications and any expert-panel (2-star+) submissions, which often come from the VCEP itself.

- **Footnote link:** `https://www.ncbi.nlm.nih.gov/clinvar/?term=<GENE>%5Bgene%5D`

## 4. OMIM phenotype line

**With an API key** (`OMIM_API_KEY` env var):
```
https://api.omim.org/api/entry?mimNumber=<MIM>&include=text:description&format=json&apiKey=<KEY>
```
Find the gene's MIM number first (NCBI Gene record, or the OMIM gene-map). Use the phenotype MIM for the disease description.

**Without a key:** cite the OMIM entry page directly, and/or the gene's GeneReviews chapter:
- `https://www.omim.org/entry/<MIM>`
- `https://www.ncbi.nlm.nih.gov/books/` (GeneReviews, search the gene)

Keep the output to one sentence: disease name and inheritance pattern. The full disease overview belongs to the `gene-brief` skill, not here.

- **Footnote link:** the OMIM entry URL, or the GeneReviews chapter URL.

## Rate limits and etiquette

- NCBI E-utilities: 3 requests/sec without a key, 10 with one. Batch PMIDs/IDs into a single esummary call rather than looping. If you hit a 429, back off and retry once.
- OMIM API: register a key at omim.org/api; without one, the entry pages are public and linkable.
- CSpec (behind the dgai-clingen MCP) needs no key.
