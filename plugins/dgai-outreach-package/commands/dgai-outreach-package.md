---
description: Produce a complete outreach package for a VCEP contact — warm path assessment, research briefing, and draft email — in a single parallel run. Synthesizes a three-section Markdown document ready for 5-minute review.
argument-hint: "[name]"
---

Produce a complete DeepGene outreach package for `$ARGUMENTS`.

If `$ARGUMENTS` is empty, stop and say: "Usage: /dgai-outreach-package [name] — e.g. /dgai-outreach-package Andy Drackley"

---

## Step 1 — Resolve the target

Read `context/known-contacts.yaml` (at `${CLAUDE_PLUGIN_ROOT}/../../../context/known-contacts.yaml`).

Find the entry whose `name` matches `$ARGUMENTS` (case-insensitive, accent-insensitive).

Extract and hold:
- `full_name` — canonical name from the YAML
- `role` and `org`
- `primary_panel` — first entry in `panels:`, or the one most relevant to variant curation if multiple
- `primary_gene` — derive from the panel name (e.g. "OTC Variant Curation Expert Panel" → `OTC`). If the panel name does not contain a clear gene symbol, leave blank and vcep-research will resolve it.
- `notes` — any special framing notes

If the name is not in the YAML, run a quick web search for "[name] ClinGen VCEP" to find their primary panel affiliation before proceeding. Note that this contact is not yet in known-contacts.yaml and recommend adding them after the package is delivered.

---

## Step 2 — Fan out three parallel sub-tasks

Send all three Task tool calls in a single message so they run concurrently. Do not wait for one before starting the others.

**Sub-task A — Warm path**

> Run the warm-path finder for this target. Execute:
> ```
> python3 "${CLAUDE_PLUGIN_ROOT}/../warm-path/scripts/warm_path.py" "[full_name]"
> ```
> (If networkx or pyyaml are missing, run `pip install networkx pyyaml` first.)
> Return the full script output verbatim — the WARM/SEED/COLD verdict, the path list, and the recommended approach block.

**Sub-task B — VCEP research briefing**

> Load and execute the `vcep-research` skill. Research target: `[primary_gene or primary_panel]`.
> Follow the skill's full procedure: resolve the panel via the dgai-clingen MCP, get the roster, pull recent ClinVar activity, pull 3–5 recent references, add the phenotype line, infer panel stage, and assemble the briefing per the template. Every claim must carry a footnote. Return the complete one-page Markdown briefing.

**Sub-task C — Draft outreach email**

> Load and execute the `dgai-outreach` skill. Target recipient: `[full_name]`, `[role]` at `[org]`, primary panel: `[primary_panel]`.
> Load all context files from the dgai-outreach and outreach-email skill directories. Follow the full procedure: research the recipient, match the offer, draft the email in Bryce's voice, run the anti-ai-ese pass. Return the complete draft email with subject line.

---

## Step 3 — Synthesize

Once all three sub-tasks return, assemble a single Markdown document with this structure:

```
# Outreach Package: [full_name]
[role], [org]
[primary_panel]
Generated: [date]

---

## 1. Warm Path

[Full output from Sub-task A, verbatim]

---

## 2. VCEP Research Briefing

[Full briefing from Sub-task B]

---

## 3. Draft Email

[Draft from Sub-task C, with subject line]

---

## Notes

- Estimated prep time for send: [X] min review
- Warm path verdict: [WARM N hops / SEED / COLD]
- Panel stage: [from briefing]
- [Any flag from known-contacts.yaml notes, e.g. "outreach parked"]
```

Apply the repo style-guide (no em dashes for parenthetical asides, no "delve"/"tapestry"/"landscape", no tricolon padding) to any prose you write in the Notes section. The sub-task outputs are returned verbatim.

Save the package as `outreach/packages/[slug]-[YYYY-MM-DD].md` in the `deepgene-operations` repo if it is mounted, otherwise output inline and tell the user where to save it.
