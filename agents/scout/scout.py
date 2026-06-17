#!/usr/bin/env python3
"""
DeepGene Skill Scout Agent
Standalone agent built on the Claude Agent SDK.

Scans marketplace sources for new skills and agents not yet in scouted.md,
scores each candidate on the standard five-column scorecard, and writes a
weekly digest to the operations repo.

Usage:
    python scout.py
    python scout.py --output-dir /path/to/notes/scout-digest
    python scout.py --dry-run     # print digest to stdout, don't write file
"""

import asyncio
import argparse
import os
import sys
from datetime import date
from pathlib import Path

from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, AssistantMessage

# ---------------------------------------------------------------------------
# Paths (relative to this file; works when repo is cloned alongside operations)
# ---------------------------------------------------------------------------

_HERE = Path(__file__).parent.resolve()
_REPO_ROOT = _HERE.parent.parent  # dgai-plugins root
_OPS_ROOT = _REPO_ROOT.parent / "deepgene-operations"

DEFAULT_OUTPUT_DIR = _REPO_ROOT / "notes" / "scout-digest"
SCOUTED_MD = _REPO_ROOT / "SCOUTED.md"
SCOUTED_MD_OPS = _OPS_ROOT / "notes" / "scouted.md"  # also checked, but not primary

# ---------------------------------------------------------------------------
# Agent configuration
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are the DeepGene skill scout agent. Your job is to find skills, agents, and
plugins that are NEW — not already catalogued in the provided scouted.md — and
score each one on the standard five-column scorecard.

You search, read, score, and report. You do not build skills or write code.

SOURCES TO CHECK (in order, stop when you have 3-5 new candidates or exhaust all sources):
1. https://github.com/anthropics/skills  — official skill repo
2. https://github.com/anthropics/claude-plugins-official  — official plugin directory
3. https://github.com/anthropics/knowledge-work-plugins  — official plugins
4. https://github.com/hesreallyhim/awesome-claude-code  — community index (skills/agents section)
5. https://github.com/hesreallyhim/a-list-of-claude-code-agents  — community agent list
6. https://github.com/travisvn/awesome-claude-skills  — curated skills index
7. https://claudemarketplaces.com  — if reachable; skip with a note if it returns no content

SCORING RUBRIC (1-5 each, 25 max):
- Docs: inputs, stop conditions, and what-not-to-use are findable without a sync
- Recency: latest commit (5=within 3 months, 3=within a year, 1=over 2 years or no date)
- License: explicit file present (5=OSI-approved, 3=permissive informal, 1=nothing)
- Fit: works in Claude Code + Python operations workflow (5=drops in, 3=minor edits, 1=wrong runtime)
- Install: cold-start effort (5=copy one file, 3=some config, 1=separate service required)

Internal skills score License as 3 (private internal, not a blocker).

OUTPUT FORMAT — return exactly this Markdown block and nothing else:

```
## Scout Digest — [DATE]

### New candidates

| # | Name | Source | Docs | Recency | License | Fit | Install | Total | Verdict |
|---|------|--------|------|---------|---------|-----|---------|-------|---------|
| 1 | ... | ... | ... | ... | ... | ... | ... | .../25 | ... |

### Recommendations

[For each candidate: USE AS-IS / ADAPT / BUILD FROM SCRATCH with 1-2 sentence reason]

### Sources checked

- [source]: [URL] — [found X new candidates / no new matches / could not fetch]

### Already catalogued (skipped)

[comma-separated list of any skills found that are already in scouted.md]
```

If no new candidates are found, write "No new candidates found this week." under
the candidates section and keep the sources-checked log.

CONSTRAINTS:
- If a page returns an empty JavaScript shell, mark it "could not fetch" and move on.
- Do not retry a URL more than once.
- Stay focused: skip anything clearly unrelated to skills, agents, or plugins for Claude Code.
- Keep it fast — aim for 3-5 sources, 3-5 candidates, done.
"""


def build_prompt(scouted_content: str, marketplace_scouted_content: str) -> str:
    today = date.today().isoformat()
    return f"""\
Today is {today}. Run the weekly skill scout pass.

=== ALREADY CATALOGUED (dgai-plugins/SCOUTED.md) ===
{scouted_content or "(file not found — treat all candidates as new)"}

=== ALSO CATALOGUED (deepgene-operations/notes/scouted.md) ===
{marketplace_scouted_content or "(file not found)"}

Search the sources listed in your instructions. For each skill or agent you find,
check whether it already appears in the catalogued sections above before scoring it.
Only score NEW items.

Return the digest in the exact Markdown format specified. Include today's date ({today})
in the heading.
"""


def read_file_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


async def run_scout(output_dir: Path, dry_run: bool = False) -> int:
    """Run the scout agent and write (or print) the digest. Returns exit code."""

    scouted = read_file_safe(SCOUTED_MD)
    scouted_ops = read_file_safe(SCOUTED_MD_OPS)
    prompt = build_prompt(scouted, scouted_ops)

    print(f"[scout] Starting agent... (model: claude-haiku-4-5)", flush=True)

    digest_lines: list[str] = []

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            model="claude-haiku-4-5-20251001",
            system_prompt=SYSTEM_PROMPT,
            allowed_tools=["WebSearch", "WebFetch", "Read"],
            permission_mode="dontAsk",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text") and block.text:
                    # Accumulate text content for the digest
                    digest_lines.append(block.text)
                elif hasattr(block, "name"):
                    print(f"[scout]   tool: {block.name}", flush=True)
        elif isinstance(message, ResultMessage):
            print(f"[scout] Agent finished ({message.subtype})", flush=True)

    # The digest is the full text output; strip fences if wrapped
    digest = "\n".join(digest_lines).strip()

    # Remove ```markdown fences if the model wrapped the output
    if digest.startswith("```"):
        lines = digest.splitlines()
        # drop first and last fence lines
        inner = []
        in_fence = False
        for line in lines:
            if line.startswith("```") and not in_fence:
                in_fence = True
                continue
            if line.startswith("```") and in_fence:
                in_fence = False
                continue
            if in_fence:
                inner.append(line)
        digest = "\n".join(inner).strip() if inner else digest

    if not digest:
        print("[scout] Warning: agent produced no output.", file=sys.stderr)
        return 1

    if dry_run:
        print("\n" + "=" * 60)
        print(digest)
        print("=" * 60)
        return 0

    # Write digest to file
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{date.today().isoformat()}.md"
    output_file.write_text(digest + "\n", encoding="utf-8")
    print(f"[scout] Digest written to {output_file}", flush=True)
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="DeepGene Skill Scout — weekly marketplace scan"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for digest files (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print digest to stdout instead of writing a file",
    )
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("[scout] Error: ANTHROPIC_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    exit_code = asyncio.run(run_scout(args.output_dir, args.dry_run))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
