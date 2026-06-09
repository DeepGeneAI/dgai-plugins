# dgai-outreach-package

One command that produces a complete outreach package for a VCEP contact. Runs three sub-tasks in parallel and returns a single Markdown document ready for a 5-minute review before sending.

## What it produces

A three-section Markdown file:

1. **Warm path** — shortest introduction route from Bryce, Amanda, or Heidi to the target, with recommended intro framing (Scenario 1 or 2 from `introduction_request_email.md`).
2. **VCEP research briefing** — one-page panel briefing: chair/coordinator, panel status and stage, recent ClinVar activity, 3–5 linked references, phenotype line. Every claim footnoted.
3. **Draft email** — first-touch outreach in Bryce's voice, Gene Report Card offer matched to the target's situation, anti-ai-ese pass applied.

## Usage

```
/dgai-outreach-package Andy Drackley
/dgai-outreach-package "Ljubica Caldovic"
```

## Dependencies

All three must be installed from the `dgai-plugins` marketplace:

- `warm-path` — graph traversal against `context/known-contacts.yaml`
- `vcep-research` + `dgai-clingen` — ClinGen MCP + ClinVar/PubMed research
- `outreach` — dgai-outreach and outreach-email skills

## How it works

The command fans out three parallel Task calls (warm path, research, email draft), waits for all three to return, then synthesizes the results into one document. End-to-end runtime target: under 90 seconds.

## Output location

If `deepgene-operations` is mounted, packages are saved to `outreach/packages/[slug]-[YYYY-MM-DD].md`. Otherwise output is inline.

## Adding contacts

If the target is not in `context/known-contacts.yaml`, the command will do a web lookup for their panel and flag them as missing from the YAML. Add them after delivering the package so future runs have a warm path.
