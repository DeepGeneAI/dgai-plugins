# warm-path

Given a target name, finds the shortest warm introduction path from any seed contact (Bryce, Amanda, Heidi) through the ClinGen/VCEP network and returns a recommended intro framing.

```
/warm-path Andy Drackley

WARM  Andy Drackley  (2 hops)

Path:
  0. Bryce Daines [seed]
     └─ direct relationship
  1. Pamela Robertson
     └─ co-panel: FBN1 Variant Curation Expert Panel
  2. Andy Drackley

Recommended approach:
  Ask Pamela Robertson for a warm intro to Andy Drackley. …
```

## How it works

The graph is built from `context/known-contacts.yaml` at the repo root. Nodes are people; edges are direct relationships, co-panel membership, or co-authorship. The script finds the shortest path using networkx BFS. Intro framing follows the scenarios in `deepgene-operations/archive/v1-2026-04-15/the-curation-table/outreach/introduction_request_email.md`.

## Verdicts

| Output | Meaning |
|---|---|
| `SEED` | Target is a seed contact — reach out directly |
| `WARM (N hops)` | Path found; connector and framing shown |
| `COLD` | Target not in YAML or not reachable from any seed |

## Maintaining the graph

Edit `context/known-contacts.yaml` by hand. No scraping. Before adding a relationship, verify it:

- `direct` — you know they have a personal or professional relationship
- `co_panel` — both appear on the same ClinGen VCEP/GCEP affiliation page
- `co_author` — confirmed via PubMed author list

Adding a node without at least one edge makes it unreachable (always COLD).

## Install

```
pip install networkx pyyaml
/plugin install warm-path@dgai-plugins
```

## Run tests

```
pytest plugins/warm-path/tests/
```

## Design notes

- **No scraping.** `known-contacts.yaml` is the source of truth.
- **Undirected graph.** Warm intros work in both directions.
- **Seeds: Bryce, Amanda, Heidi.** Paths always originate from one of these three.
- **Framing is keyed to the connector.** Amanda triggers Scenario 1; Heidi/Haendel/Saliba/Milosovich trigger Scenario 2; others get a generic ask-for-blurb prompt.
