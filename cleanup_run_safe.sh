#!/bin/bash
set -e
cd "$(dirname "$0")"

TRASH=".trash_cleanup"
mkdir -p "$TRASH"

echo "⚠️ Moving duplicates and wrappers to: $TRASH"

# Backups and trash
find . -type f \( -name "*.bak" -o -name "*pre_status*" -o -path "./backups/*" -o -path "./babbel_core/.trash.*/*" \) -exec mv -v {} "$TRASH" \;

# Orphaned scripts
[ -f scripts/or_chat_probe.py ] && mv -v scripts/or_chat_probe.py "$TRASH" || true
[ -f scripts/babbel_cli_chat.py ] && mv -v scripts/babbel_cli_chat.py "$TRASH" || true

# core/ wrappers
[ -d core ] && find core -type f -name "*.py" -exec mv -v {} "$TRASH" \;

# Extra .pyc files
find babbel_core/__pycache__ -type f -name "*.pyc" -exec mv -v {} "$TRASH" \;

# Duplicated chat.py versions
[ -f babbel_core/chat.py ] && mv -v babbel_core/chat.py "$TRASH" || true
[ -f babbel_core/anti_chatgpt_guard.py ] && mv -v babbel_core/anti_chatgpt_guard.py "$TRASH" || true

echo "✅ Cleanup complete. Moved to: $TRASH"
