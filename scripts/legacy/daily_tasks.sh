#!/bin/bash
# Daily tasks script for OpenClaw AI learning assistant
# Runs at 8:00 AM Taipei time every day

set -euo pipefail

LOG_FILE="/Users/daniel.chang/Desktop/ai/logs/daily_tasks_$(date +%Y-%m-%d).log"
CORE_LEARNING_DIR="/Users/daniel.chang/Desktop/ai/core_learning"
DAILY_UPDATES_DIR="/Users/daniel.chang/Desktop/ai/daily-updates"

# Ensure directories exist
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$CORE_LEARNING_DIR"
mkdir -p "$DAILY_UPDATES_DIR"

{
  echo "=== Daily Tasks Started: $(date) ==="

  # Phase 1: Ensure core learning files exist
  echo "--- Phase 1: Checking core learning files ---"
  core_files=(
    "01-installation-openrouter.md"
    "02-cli-commands.md"
    "03-automation.md"
    "04-agentic-workflow.md"
    "05-agentic-cron.md"
    "06-skills.md"
    "07-mcp.md"
  )

  for file in "${core_files[@]}"; do
    filepath="$CORE_LEARNING_DIR/$file"
    if [[ ! -f "$filepath" ]]; then
      echo "Creating missing file: $file"
      # Create a basic template if missing
      cat > "$filepath" <<EOF
# $file

*This file was automatically created by the daily tasks script.
Please replace this content with the appropriate learning material.*

EOF
    else
      echo "File exists: $file"
    fi
  done

  # Phase 2: Daily dynamic update
  echo "--- Phase 2: Performing daily dynamic update ---"
  TODAY=$(date +%Y-%m-%d)
  UPDATE_FILE="$DAILY_UPDATES_DIR/$TODAY.md"

  # Start the update file
  echo "# 每日動態更新 - $TODAY" > "$UPDATE_FILE"
  echo "" >> "$UPDATE_FILE"
  echo "*更新時間: $(date '+%Y-%m-%d %H:%M:%S')*" >> "$UPDATE_FILE"
  echo "" >> "$UPDATE_FILE"

  # Function to search and summarize a topic
  search_and_summarize() {
    local topic="$1"
    local section_title="$2"
    echo "## $section_title" >> "$UPDATE_FILE"
    echo "" >> "$UPDATE_FILE"
    
    # Perform web search (limit to 3 results to avoid too much content)
    openclaw web_search "$topic" --count 3 > /tmp/search_results.txt 2>/dev/null || {
      echo "搜尋失敗: $topic" >> "$UPDATE_FILE"
      echo "" >> "$UPDATE_FILE"
      return
    }
    
    # If we got results, summarize them
    if [[ -s /tmp/search_results.txt ]]; then
      openclaw summarize /tmp/search_results.txt >> "$UPDATE_FILE" 2>/dev/null || {
        # If summarise fails, just append raw results
        cat /tmp/search_results.txt >> "$UPDATE_FILE"
      }
    else
      echo "*未找到相關結果*" >> "$UPDATE_FILE"
    fi
    echo "" >> "$UPDATE_FILE"
    echo "" >> "$UPDATE_FILE"
  }

  # Search for OpenClaw latest dynamics
  search_and_summarize "OpenClaw 最新動態 2024 OpenClaw updates" "OpenClaw 最新動態"

  # Search for Agentic AI advances
  search_and_summarize "Agentic AI 新進展 2024 Agentic AI advances" "Agentic AI 新進展"

  # Search for practical cases
  search_and_summarize "AI 實際案例 2024 AI practical applications case studies" "實際案例"

  echo "=== Daily Tasks Completed: $(date) ==="
} >> "$LOG_FILE" 2>&1

# Also output to console for immediate feedback (if running interactively)
echo "Daily tasks completed. Log: $LOG_FILE"