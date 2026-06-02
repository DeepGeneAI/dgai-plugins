# vcep-research

A Claude Code plugin with one generic skill: `vcep-research`. Given a gene
symbol or a ClinGen affiliation ID, it produces a one-page, fully-cited
Markdown briefing on the relevant Curation Expert Panel.

The briefing covers: panel status and inferred stage, chair and coordinator,
scope and a one-line phenotype, recent ClinVar activity, and three to five
recent linked references. Every factual line is footnoted to a public source.

## What it pulls and from where

| Field | Source | How |
|---|---|---|
| Panel name, kind, status, scope, roster | ClinGen CSpec | `dgai-clingen` MCP (`lookup_panel`, `list_chairs`) |
| Recent variant activity | ClinVar | NCBI E-utilities (`db=clinvar`) |
| Key references | PubMed | `pubmed-database` skill if installed, else NCBI E-utilities |
| Phenotype line | OMIM / GeneReviews | OMIM API (key) or public entry page |

Query recipes live in `skills/vcep-research/context/data-sources.md`; the
output skeleton in `skills/vcep-research/context/briefing-template.md`.

## Dependencies

- **Required:** the `dgai-clingen` plugin (its MCP server `clingen` must be
  connected). Install it from this marketplace first.
- **Preferred:** the `pubmed-database` skill (K-Dense) for the literature
  step. The skill falls back to NCBI E-utilities directly when it is absent,
  so this is optional.
- **Optional:** an `OMIM_API_KEY` env var for the phenotype line. Without it
  the skill cites the public OMIM entry page and GeneReviews.

## Install

```
/plugin marketplace add DeepGeneAI/dgai-plugins
/plugin install dgai-clingen@dgai-plugins     # required dependency
/plugin install vcep-research@dgai-plugins
```

## Use

```
/vcep-research OTC
/vcep-research 50100
```

The skill resolves the gene or ID to a panel, gathers the data, and returns
the briefing. It will tell you up front if the `dgai-clingen` MCP is not
connected.

## Design notes

- **Generic, no DeepGene context.** This is the logic layer. It defines what a
  VCEP briefing is and how to build one from public data. A project framing can
  wrap it later.
- **Not the same as `recipient-research`** (in the `outreach` plugin), which
  researches a *person* for an outreach email, nor `gene-brief` (T3.7), which
  is the practitioner-level disease cover document. This skill is the upstream
  research pass on the *panel*.
- **Citations are mandatory.** A briefing with an unsourced claim is a bug.
