# Recipient research procedure (VCEP/ClinGen outreach)

The `outreach-email` skill assumes a real research pass before drafting. This file is the procedure for that pass when the recipient is a VCEP coordinator, chair, or curator. Run all four steps; capture the results so the skill's research trace can cite them.

## 1. Person background

Run the research miner to populate publications and current affiliation:

```bash
python3 the-curation-table/tools/person_research_miner.py "First Last" "ClinGen" --context outreach
```

Output lands in `the-curation-table/output/raw/`. From it, extract:

- Current title and institution (ORCID employments)
- Three to five recent publications relevant to variant curation
- Whether the recipient has a meaningful PubMed presence at all (low count is a real signal)

If ORCID returns nothing, do not block. Note it and proceed. Some curators publish under varying name forms or not at all.

## 2. Committees they chair or co-chair

The brief generator does not extract committee roles cleanly. For now, this is a manual lookup against:

- ClinGen affiliate directory: https://clinicalgenome.org/curation-activities/variant-pathogenicity/expert-panels/
- The recipient's institutional bio or LinkedIn
- Committee notes in `docs/gene-report-fact-sheet.md` if logged there

Capture each VCEP with the role explicit. A chair line lands differently than a member line. A coordinator across five panels lands differently than a chair of one. Be precise.

A future `committee_research.py` script will automate this step. Until then, do the lookup by hand.

## 3. Stage of each committee

For each VCEP from step 2, identify the stage:

- **Active curation**: submitting variants now, recent ClinVar activity from the panel
- **Protocol development**: published rules, not curating at volume yet
- **Recruiting**: early formation, building the panel
- **Dormant**: published rules but ClinVar activity has stopped
- **Unknown**: cannot tell from public sources

Stage shapes which offer fits. A panel in active curation has different needs than one in protocol development. Capture stage even when the answer is "unknown."

## 4. Gene in focus

Within the panel, which gene is the recipient currently working on? This is the per-gene angle Amanda's reply turned on. Sources, in order of preference:

1. Direct knowledge from a prior conversation (if Amanda said OTC, that is the answer)
2. The recipient's most recent first-author or senior-author paper if it names a single gene
3. A recent ClinVar submission cluster for the panel

If no single gene is identifiable, name the panel's gene set and note the gene in focus as unknown. The offer-matching step will fall back to a panel-level offer.

## What to do when data is missing

- **No ORCID, sparse PubMed**: skip publication references in the opener; lead with the panel instead
- **Cannot identify any committee**: do not send via the research-rooted path. Route via `fallbacks.md` to the project low-contact alternative.
- **Stage is unknown**: pick the offer that is panel-stage-agnostic, not the one that requires "active curation."
- **No gene in focus**: write a panel-level email, not a gene-level email. Mark the trace.

## Edge cases logged so far

- **William Craigen** — genes are somatic/cancer-related, not germline. The Gene Report offer set assumes germline curation; do not run him through this procedure. On hold (per Bryce, 2026-04-28).
- **Jason Saliba** — separate edge case. He sits on the AI committee, not the same somatic/germline issue. Standard procedure applies.
