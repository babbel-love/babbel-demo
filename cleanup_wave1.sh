#!/bin/bash
set -e
TRASH=".trash_cleanup"
mkdir -p "$TRASH"

echo "🧹 Moving backup/duplicate files..."
find . -type f \( -name "*.bak" -o -name "*pre_status*" -o -path "./backups/*" \) -exec mv -v {} "$TRASH" \;
find babbel_core -type f -name "anti_chatgpt_guard.py" -exec mv -v {} "$TRASH" \;

echo "🧹 Moving test files outside /tests/..."
find babbel_core -type f -name "test_*.py" ! -path "./babbel_core/tests/*" -exec mv -v {} "$TRASH" \;

echo "🧹 Moving old standalone scripts..."
mv -v babbel_core/node_rewrite_v2.py "$TRASH" 2>/dev/null || true
mv -v babbel_core/test_run.py "$TRASH" 2>/dev/null || true
mv -v scripts/openrouter_py_probe.py "$TRASH" 2>/dev/null || true
mv -v scripts/patch_headers.py "$TRASH" 2>/dev/null || true

echo "✅ Cleanup Wave 1 complete. Moved files to $TRASH"
