# dgai-gene-brief

DeepGene context layer on top of `gene-brief`. Produces the cover document that ships with each Gene Report Card.

## What it adds to gene-brief

- An opening framing paragraph tied to the specific report deliverable (conflicts, reclassification candidates, or VUS triage queue)
- A pain-point callout in the open questions section connecting the first question to the specific report finding

No product pitch, no CTA. The cover doc is a scientific document.

## Usage

```
/dgai-gene-brief OTC "Urea Cycle Disorders" vus_triage
/dgai-gene-brief ASS1 "Urea Cycle Disorders" reclassification_candidates
/dgai-gene-brief FBN1 "FBN1 Variant Curation Expert Panel" conflict_summary
```

Arguments: `[gene] [panel name] [pain_point: conflict_summary | reclassification_candidates | vus_triage]`

If `pain_point` is omitted, it is inferred from the evidence-code challenges section.

## Dependency

Requires the `gene-brief` plugin to be installed. Load `gene-brief/skills/gene-brief/SKILL.md` before running this skill.
