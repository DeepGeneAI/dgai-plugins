# agents/scout

Standalone Python agent that scans skill and plugin marketplaces weekly,
scores new candidates against the standard five-column scorecard, and writes
a digest to `deepgene-operations/notes/scout-digest/YYYY-MM-DD.md`.

Built on the [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview).
This is the T4.3 deliverable — promotes the Sprint 2 manual sub-agent into a
scheduled, headless agent that runs outside a Claude Code session.

---

## Prerequisites

- Python 3.10+
- `ANTHROPIC_API_KEY` set in your environment
- The `deepgene-operations` repo cloned as a sibling of `dgai-plugins`
  (i.e. `../deepgene-operations/` relative to this repo root)

---

## Setup

```bash
cd agents/scout

# Create a venv and install
python3 -m venv .venv
source .venv/bin/activate
pip install claude-agent-sdk
```

Or with `uv`:

```bash
uv venv && uv pip install claude-agent-sdk
```

---

## Run

```bash
# Standard run — writes digest to deepgene-operations/notes/scout-digest/
python scout.py

# Dry run — prints digest to stdout, no file written
python scout.py --dry-run

# Custom output directory
python scout.py --output-dir /path/to/notes/scout-digest
```

The agent completes in under 60 seconds. It uses `claude-haiku-4-5` and
limits itself to 3-5 sources per run.

---

## Weekly schedule

Install the cron entry (runs Mondays at 08:00):

```bash
bash cron_setup.sh install
```

Check status:

```bash
bash cron_setup.sh status
```

Remove:

```bash
bash cron_setup.sh uninstall
```

Logs land in `~/Library/Logs/dgai-scout.log` on macOS.

---

## What it scouts

Sources checked each run (in order):

1. `anthropics/claude-code-skills` — official skill repo
2. `anthropics/knowledge-work-plugins` — official plugins
3. `hesreallyhim/awesome-claude-code` — community index
4. `claudemarketplaces.com` — public marketplace (skipped if unreachable)

The agent reads `deepgene-operations/notes/scouted.md` and `dgai-plugins/SCOUTED.md`
before searching, so it only scores candidates that are not already catalogued.

---

## Output

Each run produces a file like `dgai-plugins/notes/scout-digest/2026-06-09.md` with:

- A scored candidate table
- Recommendations (USE AS-IS / ADAPT / BUILD FROM SCRATCH) with reasons
- A sources-checked log
- A list of already-catalogued items that were skipped

After reviewing a digest, copy any adopt/adapt picks into the main `scouted.md`
following the format in that file.

---

## Capability map

| SDK feature | Where used |
|---|---|
| `query()` agentic loop | `scout.py:run_scout()` |
| `ClaudeAgentOptions` | model, allowed_tools, permission_mode |
| `allowed_tools` | WebSearch, WebFetch, Read (read-only scout) |
| `permission_mode="dontAsk"` | headless scheduled operation |
| `ResultMessage` | detect agent completion |
| `AssistantMessage` | stream tool calls and text output |
