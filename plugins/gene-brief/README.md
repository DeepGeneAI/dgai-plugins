# gene-brief

Produces a practitioner-level cover document for a gene/VCEP. Intended to ship as the cover document with a Gene Report Card or as standalone research ahead of a call.

## What it produces

A two-to-three page Markdown document with five sections:

1. **Disease overview** — inheritance, clinical spectrum, biochemistry, population frequency
2. **VCEP protocol status** — current CSpec version, gene-specific code modifications as a table
3. **Evidence-code challenges** — per-code analysis of where classification is genuinely hard for this gene (4–6 codes)
4. **Classification-relevant literature** — 5–7 papers directly bearing on variant classification
5. **Open questions** — 3–5 specific unresolved tensions a curator would immediately recognize

## How it differs from vcep-research

`vcep-research` answers: "what is this panel and is it active?" (panel metadata, roster, ClinVar activity count, brief ref list)

`gene-brief` answers: "what does a curator need to know to classify variants in this gene?" (disease biology, evidence-code deep-dive, classification challenges, open questions)

Run vcep-research first for panel metadata; run gene-brief for the scientific layer.

## Usage

Load the `gene-brief` skill and provide a gene symbol:

```
/gene-brief OTC
/gene-brief ASS1
/gene-brief FBN1
```

For a Gene Report cover document with DeepGene framing, use the `dgai-gene-brief` skill instead.

## Examples

- `examples/otc-gene-brief.md` — OTC/ornithine transcarbamylase deficiency
- `examples/ass1-gene-brief.md` — ASS1/citrullinemia type I
