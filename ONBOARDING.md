# DeepGene Plugins — Onboarding

This document gets you from zero to running the outreach pipeline in half a day. It covers environment setup, plugin installation, what each plugin does, how the pipeline works end to end, how to read the KPI dashboard, and the design constraints that apply to every task.

---

## What this repo is

`deepgene-plugins` is the private Claude Code plugin marketplace for DeepGene. It ships plugins that Claude uses to research VCEP contacts, draft outreach, and track pipeline metrics. It is the distribution channel for all Claude capabilities built at DeepGene.

The companion repo `deepgene-operations` holds project artifacts (outreach drafts, gene briefs, intake schemas, tracker). The two repos are distinct: `dgai-plugins` is the toolbox; `deepgene-operations` is the workbench.

---

## Prerequisites

**Tools.** You need these before anything else works:

```bash
# Verify each before continuing
claude --version        # Claude Code CLI, must be authenticated
node --version          # Node 20+
python3 --version       # Python 3.11+
pip install networkx pyyaml gspread google-auth-oauthlib
```

**Repos.** Clone both into the same parent directory:

```bash
git clone git@github.com:DeepGeneAI/dgai-plugins.git
git clone git@github.com:DeepGeneAI/deepgene-operations.git
```

**Cowork.** Open the Claude desktop app. Enable Cowork mode. Both repos should appear as mounted folders.

**Marketplace.** Register the private marketplace in Claude Code once:

```bash
/plugin marketplace add DeepGeneAI/dgai-plugins
```

Confirm it appears in `/plugin` → Discover.

---

## Plugin inventory

### `dgai-hello`
Smoke test for marketplace installs. Run `/dgai-hello Bryce` — if it returns "Hello, Bryce. The plumbing works," the marketplace is wired correctly. Use this after any machine setup.

### `dgai-clingen`
MCP server exposing two tools against the public ClinGen CSpec Registry: `lookup_panel(gene_or_id)` and `list_chairs(affiliation_id)`. No API key required. Required by `vcep-research` and `dgai-outreach-package`.

```bash
/plugin install dgai-clingen@dgai-plugins
```

### `vcep-research`
Generic skill. Given a gene symbol or ClinGen affiliation ID, returns a one-page Markdown briefing: panel status and stage, chair/coordinator, scope, recent ClinVar activity, 3–5 linked references. Every claim has a footnote. Requires `dgai-clingen` installed.

```bash
/plugin install dgai-clingen@dgai-plugins   # dependency
/plugin install vcep-research@dgai-plugins
/vcep-research OTC
/vcep-research 50100
```

### `outreach`
Four skills in one plugin:

| Skill | Layer | What it does |
|---|---|---|
| `outreach-email` | Generic | Research-rooted first-touch email for any recipient |
| `dgai-outreach` | DeepGene | Wraps `outreach-email` with Gene Report framing and Bryce's voice |
| `followup-email` | Generic | Post-delivery follow-up referencing specific report content |
| `dgai-followup` | DeepGene | Wraps `followup-email` with DeepGene context |

```bash
/plugin install outreach@dgai-plugins
/dgai-outreach "Ljubica Caldovic"
/dgai-followup "Amanda Thomas Wilson"
```

### `warm-path`
Given a target name, returns the shortest introduction path from seed contacts (Bryce, Amanda, Heidi) through the ClinGen network, with recommended intro framing. Reads `context/known-contacts.yaml` as source of truth — no scraping.

```bash
/plugin install warm-path@dgai-plugins
/warm-path "Andy Drackley"
```

Possible outputs: `SEED` (direct), `WARM (N hops)` (path found), `COLD` (not reachable). Add new contacts to `context/known-contacts.yaml` after each outreach run.

### `dgai-outreach-package`
The pipeline command. Fans out three parallel sub-tasks — warm path, VCEP research, email draft — and returns a single Markdown document ready for a 5-minute review. Target runtime: under 90 seconds.

```bash
/plugin install warm-path@dgai-plugins
/plugin install vcep-research@dgai-plugins
/plugin install dgai-clingen@dgai-plugins
/plugin install outreach@dgai-plugins
# dgai-outreach-package not yet in marketplace.json — load from local path:
# /plugin install ./plugins/dgai-outreach-package
/dgai-outreach-package "Ljubica Caldovic"
```

If `deepgene-operations` is mounted, the package is saved to `outreach/packages/[slug]-[YYYY-MM-DD].md`. Otherwise it prints inline.

**Note:** This plugin is built but not yet registered in `marketplace.json`. Add it before the Sprint 3 phase gate.

### `gene-brief` and `dgai-gene-brief`
Practitioner-level gene cover documents. `gene-brief` is the generic layer (disease overview, VCEP protocol status, evidence-code challenges, classification literature, open questions). `dgai-gene-brief` wraps it with DeepGene framing for a specific panel.

```bash
/gene-brief OTC
/dgai-gene-brief ASS1
```

These differ from `vcep-research`: `vcep-research` answers "what is this panel?" while `gene-brief` answers "what does a curator need to know to classify variants in this gene?" Run `vcep-research` first, then `gene-brief` for the science layer.

**Note:** These plugins are built but not yet registered in `marketplace.json`.

### `skill-scout`
Sub-agent that searches external sources (Anthropic skill repos, `awesome-claude-code`, community marketplaces) for existing skills before you build new ones. Returns a scored candidate table. Run this before opening any new `SKILL.md`.

```bash
/plugin install skill-scout@dgai-plugins
# Then use via the Task tool or trigger the skill directly
```

### `dgai-instrumentation` / `invocation-log`
`PostToolUse` hook that logs every skill invocation to `~/.claude/dgai-skill-invocations.jsonl`. Install on every machine that runs skills so the KPI data is captured. Both plugins do the same thing; `dgai-instrumentation` is the current canonical one.

```bash
/plugin install dgai-instrumentation@dgai-plugins
```

---

## The outreach pipeline end to end

A complete outreach run for one contact:

1. **Check the warm path.** `/warm-path "[Target Name]"` — confirms whether you have an intro route and who to ask.

2. **Run the package command.** `/dgai-outreach-package "[Target Name]"` — produces warm path + VCEP briefing + draft email in one shot. Review the output at `deepgene-operations/outreach/packages/`.

3. **5-minute review.** Check: does the email reference something specific about their panel? Is the offer matched to their stage? Is the intro framing correct for the connector (Amanda = Scenario 1, Heidi/Haendel = Scenario 2)?

4. **Send.** Bryce sends. Log the send by incrementing `outreach_packages_sent` in `METRICS.md` and running `python3 scripts/update-metrics.py --sync-sheets`.

5. **Add the contact to the YAML.** Update `context/known-contacts.yaml` with any new edges you confirmed during research.

6. **Follow up at 5 business days.** `/dgai-followup "[Target Name]"` — references specific content from the delivered report.

---

## The KPI dashboard

The Monday morning dashboard lives in Cowork as a live artifact (`kpi-dashboard`). Open it from the Cowork sidebar. It reads live from the [DeepGene Plugin KPIs Google Sheet](https://docs.google.com/spreadsheets/d/1Sr5ccK7UQl83qPq6d7CaJVVeuxSX8PNfv9beb_vWDA8).

**To refresh the data:**

```bash
cd /path/to/dgai-plugins
python3 scripts/update-metrics.py --sync-sheets
```

Run this after any batch of skill usage. The script reads `~/.claude/dgai-skill-invocations.jsonl`, recomputes the metrics, updates `METRICS.md`, and pushes to the Sheet. The artifact pulls fresh data on the next open.

**Manual counters** (`outreach_packages_sent`, `responses_received`) are edited directly in `METRICS.md` and synced with the same script.

**What the dashboard shows:**
- Skills published in marketplace
- Outreach packages sent and responses received
- Invocations per skill (last 7 days) — sorted by volume with bar chart
- Inactive skills (no invocations in 2 weeks) — flagged in yellow; these are candidates for review or retirement

---

## Design constraints

These apply to every task. A deliverable that violates them gets refactored before the PR is merged.

**1. Logic vs. context separation.** Every skill ships in two layers: a generic logic layer (reusable by any project) and a DeepGene context layer (injected at runtime). The generic layer defines *what* the skill does. The context layer defines DeepGene's situation, voice, and offer. They live in separate directories and never merge. `outreach-email` and `dgai-outreach` are the reference implementation.

**2. Find before build.** Before opening a new `SKILL.md`, run the `skill-scout` sub-agent against the capability you need. Check `anthropics/skills`, `awesome-claude-code`, and `claudemarketplaces.com`. Document what exists in `SCOUTED.md` before writing a line. Half of new capabilities should be installs or forks, not original builds.

**3. Markdown first.** Default output for all deliverables is `.md`. Produce `.docx` or `.pdf` only when the consumer cannot read Markdown. This applies to skills, briefs, templates, and cover documents.

**4. Anti-AI-ese.** No em dashes for parenthetical asides. No "delve," "tapestry," "landscape," "in today's fast-paced world," "it's important to note," "it's worth noting." No tricolon padding ("clear, concise, and compelling"). No hedging adverbs ("genuinely," "honestly"). The full rules are in `deepgene-operations/.claude/skills/anti-ai-ese/SKILL.md` and in `deepgene-operations/the-curation-table/style/anti-ai-ese-style-guide.md`. Apply them before returning any draft. The `outreach` plugin loads the style guide directly as a mandatory step.

**5. Citations mandatory.** Any skill that surfaces a fact, claim, or recommendation links the source. Briefings include footnoted references. Outreach emails reference a specific paper or panel record by URL. An unsourced claim is a bug.

**6. PR-gated completion.** A task is complete when its PR is merged. Slack messages and screenshots do not count.

---

## Where things live

| Item | Location |
|---|---|
| Reading log | `deepgene-operations/notes/reading-log.md` |
| Skill scout results | `dgai-plugins/SCOUTED.md` |
| KPI metrics | `dgai-plugins/METRICS.md` |
| Invocation log | `~/.claude/dgai-skill-invocations.jsonl` (local, not committed) |
| Known contacts graph | `dgai-plugins/context/known-contacts.yaml` |
| Outreach examples | `dgai-plugins/examples/outreach/` |
| Gene brief examples | `dgai-plugins/plugins/gene-brief/examples/` |
| VCEP research examples | `dgai-plugins/plugins/vcep-research/examples/` |
| Intake schema | `deepgene-operations/intake/schema.yaml` |
| Tracker | `deepgene-operations/tracker.md` |
| Style guide | `deepgene-operations/the-curation-table/style/anti-ai-ese-style-guide.md` |
