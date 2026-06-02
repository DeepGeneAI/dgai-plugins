# VCEP briefing template

The `vcep-research` skill returns one page of Markdown in this shape. Every factual line ends in a footnote marker. Fill what the data supports; mark anything you could not resolve as `unknown` rather than guessing.

## Panel stage taxonomy

Classify the panel stage from CSpec status plus ClinVar activity (step 6 of the procedure). This matches the taxonomy the `outreach` plugin's `recipient-research.md` uses, so the two stay consistent:

- **Active curation** — submitting variants now; recent ClinVar activity from the panel
- **Protocol development** — published criteria, not curating at volume yet
- **Recruiting** — early formation; little or no CSpec spec
- **Dormant** — published rules but ClinVar activity has stopped
- **Unknown** — cannot tell from public sources

## Output skeleton

```markdown
# VCEP Briefing: <GENE> — <Panel name>

**Panel ID:** <affiliation_id> · **Type:** <VCEP|GCEP> · **ClinGen:** <url>
**Prepared:** <YYYY-MM-DD> · **Sources:** ClinGen/CSpec, ClinVar, PubMed<, OMIM>

## Status and stage
- **CSpec status:** <status>[^1]
- **Inferred stage:** <active curation | protocol development | recruiting | dormant | unknown> — <one line of justification from the ClinVar/status signal>[^2]

## Chairs and coordinator
- **Chair:** <name>, <institution>[^3]
- **Coordinator:** <name>, <institution> (or "none listed in CSpec")[^3]

## Scope and phenotype
- **Scope:** <panel scope from CSpec>[^1]
- **Phenotype:** <disease name, inheritance pattern, one sentence>[^4]

## Recent ClinVar activity
- <Total variants>, <N modified in the last 2 years>; significance breakdown <…>; <note any recent reclassifications or expert-panel submissions>[^5]

## Key literature
1. <First-author Last et al., Year> — <one line on why it matters for classification>[^6]
2. …
(three to five entries)

## References
[^1]: ClinGen/CSpec — <url>
[^2]: <ClinVar gene view + CSpec status used for the inference>
[^3]: ClinGen affiliation — <url>
[^4]: OMIM/GeneReviews — <url>
[^5]: ClinVar — https://www.ncbi.nlm.nih.gov/clinvar/?term=<GENE>%5Bgene%5D
[^6]: https://pubmed.ncbi.nlm.nih.gov/<PMID>/
```

## Rules

- **One page.** If it runs longer, the literature list is too long or the prose is padded. Trim to the three to five references that matter.
- **Every fact footnoted.** A line without a citation is a line to cut or source.
- **`unknown` is a valid value.** A briefing that honestly marks two fields unknown beats one that guesses them.
- **Voice.** Apply the repo `style-guide.md` before returning: no em-dash asides, no banned filler words, no tricolon padding.
