# Report Content Framing — How to Write Specific References

The acceptance bar for a follow-up email is: the reference to the report content
is specific, not generic. This file defines what "specific" means for each of the
four Gene Report products and shows examples of how to phrase it.

---

## What "specific" means

Generic (not acceptable):
> "I hope you found the report useful."
> "The report surfaced some interesting findings."
> "Let me know if you have any questions about the results."

Specific (required):
> "The reclassification candidates section flagged 4 variants within one evidence criterion of likely pathogenic — ASS1:c.421-2A>G looks particularly close given the functional data in the 2023 Häberle paper."
> "The conflict summary identified 2 submitters with LP calls that conflict with your Expert Panel's VUS — both have published papers that may resolve them."
> "The VUS triage queue put 8 variants in the top tier — all have functional evidence in the literature that hasn't been formally curated yet."

---

## Per-product framing

### reclassification_candidates

Lead with:
1. The count of variants flagged near a threshold
2. One specific variant by name (HGVS notation preferred) if available
3. The evidence type that would tip it, or the paper that contains relevant evidence

Template: "The reclassification candidates section flagged [N] variants within one evidence criterion of [LP/LB] — [VARIANT] looks [closest / most actionable] given [EVIDENCE_TYPE] in [PAPER or 'available literature']."

If the report hasn't been seen yet (drafting in advance of delivery): use the template with bracketed placeholders and note that these need to be filled from the actual report before sending.

### conflict_summary

Lead with:
1. The count of active conflicts
2. Whether any have published papers that may resolve them (that's the actionable subset)
3. One specific lab name or submission date if available

Template: "The conflict summary found [N] active conflicts with other ClinVar submitters — [M] of them have published papers that may resolve the discrepancy."

### vus_triage

Lead with:
1. Total VUS in the gene
2. How many landed in the top tier (actionable now)
3. What made the top-tier variants actionable (evidence type, proximity to threshold)

Template: "The VUS triage queue ranked [total] variants — [N] in the top tier, all with [functional / segregation / population] evidence in the literature that hasn't been incorporated into a formal curation."

### per_paper_summaries

Lead with:
1. The variants covered
2. One specific paper and what it found
3. Which ACMG criterion the finding would support

Template: "The per-paper summaries for [VARIANT] include [PAPER], which describes [FINDING] — that's potential [EVIDENCE_CODE] evidence if the panel applies [relevant gene-specific rule]."

---

## What to do when report content isn't yet available

If the report hasn't been delivered yet and you're drafting the follow-up in advance
(e.g., as part of a pipeline), use the templates above with clear bracketed
placeholders. Do not send a follow-up without filling in the placeholders from
the actual report. A generic reference is worse than no follow-up at all.

Mark the draft with a header: `[DRAFT — fill in report specifics before sending]`
