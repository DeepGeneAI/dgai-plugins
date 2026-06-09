#!/usr/bin/env python3
"""PostToolUse hook: append one JSONL row per unique Skill invocation.

Reads the Claude Code PostToolUse JSON payload from stdin, extracts the
skill name and plugin namespace, and appends a row to
~/.claude/dgai-skill-invocations.jsonl.

Deduplication: if the same skill was already logged in this session within
the last 60 seconds, the row is silently dropped. This enforces the KPI
definition: one counted invocation per slash command per session per
60-second window.

Always exits 0 — a logger bug must never block a tool call.
"""
import datetime
import json
import pathlib
import sys

LOG_PATH = pathlib.Path.home() / ".claude" / "dgai-skill-invocations.jsonl"
DEDUP_WINDOW_SECONDS = 60


def estimate_tokens(obj) -> int:
    return max(1, len(json.dumps(obj, default=str)) // 4)


def is_duplicate(skill_name: str, session_id: str) -> bool:
    """Return True if this skill was already logged in this session within the window."""
    if not LOG_PATH.exists():
        return False
    cutoff = datetime.datetime.now(datetime.timezone.utc).timestamp() - DEDUP_WINDOW_SECONDS
    try:
        with LOG_PATH.open(encoding="utf-8") as f:
            for line in f:
                try:
                    row = json.loads(line)
                    if (row.get("skill_name") == skill_name
                            and row.get("session_id") == session_id
                            and row.get("timestamp")):
                        ts = datetime.datetime.fromisoformat(row["timestamp"]).timestamp()
                        if ts >= cutoff:
                            return True
                except Exception:
                    continue
    except Exception:
        pass
    return False


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    if payload.get("tool_name") != "Skill":
        return 0

    tool_input = payload.get("tool_input") or {}
    tool_response = payload.get("tool_response") or {}
    session_id = payload.get("session_id", "")

    skill_ref = (tool_input.get("skill") or "").strip()
    if ":" in skill_ref:
        plugin, _, skill_name = skill_ref.partition(":")
    else:
        plugin, skill_name = "", skill_ref

    if not skill_name:
        return 0

    if is_duplicate(skill_name, session_id):
        return 0

    row = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "session_id": session_id,
        "skill_name": skill_name,
        "plugin": plugin or None,
        "input_tokens_estimate": estimate_tokens(tool_input),
        "output_tokens_estimate": estimate_tokens(tool_response),
    }

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
