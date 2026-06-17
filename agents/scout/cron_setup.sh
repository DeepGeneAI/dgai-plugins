#!/usr/bin/env bash
# cron_setup.sh — configure a weekly cron job for the skill scout agent
#
# Usage:
#   bash cron_setup.sh install    # add the weekly cron entry
#   bash cron_setup.sh uninstall  # remove it
#   bash cron_setup.sh status     # show current entry if any
#
# The cron fires every Monday at 08:00 local time.
# Logs land in ~/Library/Logs/dgai-scout.log (macOS) or /var/log/dgai-scout.log.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCOUT_PY="$SCRIPT_DIR/scout.py"
PYTHON_BIN="${PYTHON_BIN:-$(which python3)}"
LOG_FILE="${HOME}/Library/Logs/dgai-scout.log"
CRON_MARKER="# dgai-scout"

# Monday 08:00 — adjust CRON_SCHEDULE to taste (e.g. "0 8 * * 1" = Mon 8am)
CRON_SCHEDULE="0 8 * * 1"
CRON_ENTRY="$CRON_SCHEDULE $PYTHON_BIN $SCOUT_PY >> $LOG_FILE 2>&1 $CRON_MARKER"

cmd="${1:-help}"

case "$cmd" in
  install)
    # Remove any existing entry first
    (crontab -l 2>/dev/null | grep -v "$CRON_MARKER") | crontab - || true
    # Add the new entry
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo "Installed: $CRON_ENTRY"
    echo "Log: $LOG_FILE"
    ;;
  uninstall)
    (crontab -l 2>/dev/null | grep -v "$CRON_MARKER") | crontab - || true
    echo "Removed dgai-scout cron entry."
    ;;
  status)
    entry=$(crontab -l 2>/dev/null | grep "$CRON_MARKER" || echo "(not installed)")
    echo "$entry"
    ;;
  help|*)
    echo "Usage: $0 [install|uninstall|status]"
    ;;
esac
