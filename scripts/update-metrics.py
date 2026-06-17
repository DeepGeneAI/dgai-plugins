#!/usr/bin/env python3
"""Regenerate the auto-generated stats section of METRICS.md.

Reads ~/.claude/dgai-skill-invocations.jsonl, computes invocations per
skill per week, and rewrites the <!-- METRICS:START --> … <!-- METRICS:END -->
block in METRICS.md at the repo root.

Manual counters (outreach_packages_sent, etc.) live above that block
and are never touched.

Usage:
    python3 scripts/update-metrics.py                  # update METRICS.md only
    python3 scripts/update-metrics.py --sync-sheets    # also sync to Google Sheet

Google Sheets sync (first run only):
    pip install gspread google-auth-oauthlib
    Download OAuth2 Desktop credentials from Google Cloud Console and save to
    ~/.config/gspread/credentials.json
    On first run with --sync-sheets, a browser window will open to authorize.
    Subsequent runs use the saved token automatically.

Sheet ID is read from the DGAI_SHEET_ID environment variable, or falls back
to the hardcoded default below.
"""
import argparse
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

# Sheet created 2026-06-16. Override with DGAI_SHEET_ID env var.
DEFAULT_SHEET_ID = "1Sr5ccK7UQl83qPq6d7CaJVVeuxSX8PNfv9beb_vWDA8"


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


def read_manual_counters():
    """Parse outreach_packages_sent and responses_received from METRICS.md."""
    counters = {"outreach_packages_sent": 0, "responses_received": 0}
    if not METRICS_MD.exists():
        return counters
    content = METRICS_MD.read_text(encoding="utf-8")
    for key in counters:
        m = re.search(rf"\|\s*{key}\s*\|\s*(\d+)\s*\|", content)
        if m:
            counters[key] = int(m.group(1))
    return counters


def sync_to_sheets(rows, published, sheet_id):
    """Write Summary and Invocations tabs to the Google Sheet via gspread."""
    try:
        import gspread
    except ImportError:
        print(
            "gspread not installed. Run: pip install gspread google-auth-oauthlib",
            file=sys.stderr,
        )
        return

    try:
        gc = gspread.oauth()
    except Exception as e:
        print(f"Sheets auth failed: {e}", file=sys.stderr)
        return

    sh = gc.open_by_key(sheet_id)
    now = datetime.datetime.now(datetime.timezone.utc)
    weekly = invocations_per_skill_per_week(rows)
    inactive = inactive_skills(rows, published)
    manual = read_manual_counters()

    # --- Summary tab ---
    try:
        ws = sh.worksheet("Summary")
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title="Summary", rows=10, cols=2)

    ws.clear()
    ws.update(
        range_name="A1",
        values=[
            ["key", "value"],
            ["last_updated", now.isoformat()],
            ["skills_published", len(published)],
            ["invocations_last_7d", json.dumps(weekly)],
            ["inactive_skills", json.dumps(inactive)],
            ["outreach_packages_sent", manual["outreach_packages_sent"]],
            ["responses_received", manual["responses_received"]],
        ],
    )
    print("  Summary tab updated.")

    # --- Invocations tab ---
    try:
        ws_inv = sh.worksheet("Invocations")
    except gspread.exceptions.WorksheetNotFound:
        ws_inv = sh.add_worksheet(title="Invocations", rows=1000, cols=6)

    ws_inv.clear()
    headers = ["timestamp", "session_id", "skill_name", "plugin",
               "input_tokens_estimate", "output_tokens_estimate"]
    inv_rows = [headers] + [
        [
            r.get("timestamp", ""),
            r.get("session_id", ""),
            r.get("skill_name", ""),
            r.get("plugin", "") or "",
            r.get("input_tokens_estimate", ""),
            r.get("output_tokens_estimate", ""),
        ]
        for r in rows
    ]
    ws_inv.update(range_name="A1", values=inv_rows)
    print(f"  Invocations tab updated ({len(rows)} rows).")
    print(f"  Sheet: https://docs.google.com/spreadsheets/d/{sheet_id}")


def main():
    parser = argparse.ArgumentParser(description="Update METRICS.md and optionally sync to Google Sheets.")
    parser.add_argument(
        "--sync-sheets",
        action="store_true",
        help="Also sync metrics to the Google Sheet.",
    )
    parser.add_argument(
        "--sheet-id",
        default=None,
        help="Google Sheet ID to sync to (overrides DGAI_SHEET_ID env var and default).",
    )
    args = parser.parse_args()

    rows = load_invocations()
    published = skills_published()
    stats = build_stats_block(rows, published)
    update_metrics_md(stats)
    print(f"  {len(rows)} deduplicated invocations · {len(published)} skills published")

    if args.sync_sheets:
        import os
        sheet_id = args.sheet_id or os.environ.get("DGAI_SHEET_ID") or DEFAULT_SHEET_ID
        print(f"  Syncing to Sheet {sheet_id}...")
        sync_to_sheets(rows, published, sheet_id)


if __name__ == "__main__":
    main()
