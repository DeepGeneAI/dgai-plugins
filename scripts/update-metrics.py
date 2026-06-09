#!/usr/bin/env python3
"""Regenerate the auto-generated stats section of METRICS.md.

Reads ~/.claude/dgai-skill-invocations.jsonl, computes invocations per
skill per week, and rewrites the <!-- METRICS:START --> … <!-- METRICS:END -->
block in METRICS.md at the repo root.

Manual counters (outreach_packages_sent, etc.) live above that block
and are never touched.

Usage:
    python3 scripts/update-metrics.py
"""
import datetime
import json
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).parent.parent
METRICS_MD = REPO_ROOT / "METRICS.md"
LOG_PATH = pathlib.Path.home() / ".claude" / "dgai-skill-invocations.jsonl"
MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"

DEDUP_WINDOW_SECONDS = 60
INACTIVE_WEEKS = 2


def load_invocations():
    """Load and deduplicate rows from the skill invocations log."""
    if not LOG_PATH.exists():
        return []
    rows = []
    try:
        with LOG_PATH.open(encoding="utf-8") as f:
            for line in f:
                try:
                    rows.append(json.loads(line.strip()))
                except Exception:
                    continue
    except Exception:
        return []

    # Deduplicate: same skill + session within 60-second window
    seen = {}  # (skill_name, session_id) -> last_timestamp
    deduped = []
    for row in sorted(rows, key=lambda r: r.get("timestamp", "")):
        key = (row.get("skill_name", ""), row.get("session_id", ""))
        ts_str = row.get("timestamp", "")
        try:
            ts = datetime.datetime.fromisoformat(ts_str).timestamp()
        except Exception:
            continue
        last = seen.get(key)
        if last is not None and (ts - last) < DEDUP_WINDOW_SECONDS:
            continue
        seen[key] = ts
        deduped.append(row)
    return deduped


def skills_published():
    """Return list of skill names from marketplace.json."""
    try:
        with MARKETPLACE.open() as f:
            m = json.load(f)
        return [p["name"] for p in m.get("plugins", [])]
    except Exception:
        return []


def invocations_per_skill_per_week(rows):
    """Return dict: skill_name -> count in the last 7 days."""
    cutoff = datetime.datetime.now(datetime.timezone.utc).timestamp() - 7 * 86400
    counts = {}
    for row in rows:
        try:
            ts = datetime.datetime.fromisoformat(row["timestamp"]).timestamp()
        except Exception:
            continue
        if ts >= cutoff:
            skill = row.get("skill_name", "unknown")
            counts[skill] = counts.get(skill, 0) + 1
    return counts


def inactive_skills(rows, published):
    """Return skills with zero invocations in the last INACTIVE_WEEKS weeks."""
    cutoff = datetime.datetime.now(datetime.timezone.utc).timestamp() - INACTIVE_WEEKS * 7 * 86400
    active = set()
    for row in rows:
        try:
            ts = datetime.datetime.fromisoformat(row["timestamp"]).timestamp()
        except Exception:
            continue
        if ts >= cutoff:
            active.add(row.get("skill_name", ""))
    return [s for s in published if s not in active]


def build_stats_block(rows, published):
    now = datetime.datetime.now(datetime.timezone.utc)
    weekly = invocations_per_skill_per_week(rows)
    inactive = inactive_skills(rows, published)

    lines = [
        f"<!-- METRICS:START -->",
        f"*Last updated: {now.strftime('%Y-%m-%d %H:%M UTC')}*",
        "",
        "## Skills published",
        "",
        f"**{len(published)}** plugins in marketplace",
        "",
    ]
    for s in published:
        lines.append(f"- {s}")

    lines += [
        "",
        "## Invocations — last 7 days",
        "",
    ]
    if weekly:
        lines.append("| Skill | Invocations |")
        lines.append("|---|---|")
        for skill, count in sorted(weekly.items(), key=lambda x: -x[1]):
            lines.append(f"| {skill} | {count} |")
    else:
        lines.append("*No invocations recorded yet.*")

    lines += [
        "",
        "## Inactive skills (no invocations in last 2 weeks)",
        "",
    ]
    if inactive:
        for s in inactive:
            lines.append(f"- ⚠ {s}")
    else:
        lines.append("*All published skills used in the last 2 weeks.*")

    lines += ["", "<!-- METRICS:END -->"]
    return "\n".join(lines)


def update_metrics_md(stats_block):
    if not METRICS_MD.exists():
        print(f"METRICS.md not found at {METRICS_MD}", file=sys.stderr)
        sys.exit(1)

    content = METRICS_MD.read_text(encoding="utf-8")
    pattern = re.compile(
        r"<!-- METRICS:START -->.*?<!-- METRICS:END -->",
        re.DOTALL,
    )
    if pattern.search(content):
        updated = pattern.sub(stats_block, content)
    else:
        updated = content.rstrip() + "\n\n" + stats_block + "\n"

    METRICS_MD.write_text(updated, encoding="utf-8")
    print(f"Updated {METRICS_MD}")


def main():
    rows = load_invocations()
    published = skills_published()
    stats = build_stats_block(rows, published)
    update_metrics_md(stats)
    print(f"  {len(rows)} deduplicated invocations · {len(published)} skills published")


if __name__ == "__main__":
    main()
