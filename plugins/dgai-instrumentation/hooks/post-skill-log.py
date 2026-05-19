#!/usr/bin/env python3
"""PostToolUse hook: append one JSONL row per Skill invocation.

Reads the Claude Code PostToolUse JSON payload from stdin, extracts the
skill name and plugin namespace, estimates token counts, and appends a row
to ~/.claude/dgai-invocations.jsonl. Always exits 0 so a logger bug never
blocks a tool call. Seed data for the Sprint 4 KPI dashboard.
"""
import json
import sys
import datetime
import pathlib


def estimate_tokens(obj) -> int:
    # Crude ~4 chars/token heuristic. Good enough to seed KPIs;
    # swap in tiktoken later if Sprint 4 needs real numbers.
    return max(1, len(json.dumps(obj, default=str)) // 4)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    if payload.get("tool_name") != "Skill":
        return 0

    tool_input = payload.get("tool_input") or {}
    tool_response = payload.get("tool_response") or {}
    skill_ref = (tool_input.get("skill") or "").strip()
    if ":" in skill_ref:
        plugin, _, skill_name = skill_ref.partition(":")
    else:
        plugin, skill_name = "", skill_ref

    row = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "skill_name": skill_name,
        "plugin": plugin or None,
        "input_tokens_estimate": estimate_tokens(tool_input),
        "output_tokens_estimate": estimate_tokens(tool_response),
    }

    log_path = pathlib.Path.home() / ".claude" / "dgai-invocations.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
