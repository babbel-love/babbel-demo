#!/bin/bash
set -e
TRASH=".trash_cleanup"
mkdir -p "$TRASH"

echo "🧹 Removing .DS_Store and stray log files..."
find . -name ".DS_Store" -exec mv -v {} "$TRASH" \;
find . -name "streamlit.out.*" -exec mv -v {} "$TRASH" \;
mv -v streamlit.pid "$TRASH" 2>/dev/null || true
mv -v latest_ci_log.txt "$TRASH" 2>/dev/null || true
mv -v ci_failure_log.txt "$TRASH" 2>/dev/null || true
mv -v duplicates_*.txt "$TRASH" 2>/dev/null || true
mv -v events.jsonl "$TRASH" 2>/dev/null || true
mv -v file_structure.txt "$TRASH" 2>/dev/null || true

echo "🧹 Removing empty or trash folders..."
rm -rf ./exports ./backups ./babbel_core/.quarantine_headers ./babbel_core/.trash.* || true

echo "🧹 (Optional) Move unused folders to trash (manual review after):"
mv -v babbel_core/_quarantine_manual "$TRASH" 2>/dev/null || true
mv -v babbel_core/adapters "$TRASH" 2>/dev/null || true
mv -v babbel_core/scripts "$TRASH" 2>/dev/null || true
mv -v babbel_core/babbel_core.egg-info "$TRASH" 2>/dev/null || true

echo "✅ Cleanup Wave 3 complete. Review $TRASH before permanent delete."
