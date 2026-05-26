#!/usr/bin/env bash
# dgai statusline — model · context · today's invocations · active plugins
# Copy to ~/.claude/statusline.sh and chmod +x

input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name // "—"')
CTX=$(echo "$input"   | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

# Today's invocation count from the hook logger JSONL
TODAY=$(date +%Y-%m-%d)
LOG="$HOME/.claude/dgai-invocations.jsonl"
if [[ -f "$LOG" ]]; then
  INV=$(grep -c "\"$TODAY" "$LOG" 2>/dev/null || echo 0)
else
  INV=0
fi

# Active plugin count — count installed plugin directories
PLUGIN_DIR="$HOME/.claude/plugins"
if [[ -d "$PLUGIN_DIR" ]]; then
  PLUGINS=$(find "$PLUGIN_DIR" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ')
else
  PLUGINS=0
fi

echo "[$MODEL] ${CTX}% ctx  ·  ${INV} inv today  ·  ${PLUGINS} plugins"
