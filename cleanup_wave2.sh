#!/bin/bash
set -e
TRASH=".trash_cleanup"
mkdir -p "$TRASH"

echo "🧹 Moving experimental/quarantine modules..."
[ -d babbel_core/_quarantine ] && mv -v babbel_core/_quarantine "$TRASH" || true
[ -d babbel_core/core ] && mv -v babbel_core/core "$TRASH" || true

echo "🧹 Moving scratch or deprecated single-file helpers..."
mv -v babbel_core/_import_shim.py "$TRASH" 2>/dev/null || true
mv -v babbel_core/_auth_diag.py "$TRASH" 2>/dev/null || true
mv -v babbel_core/memory_anchor.py "$TRASH" 2>/dev/null || true

echo "🧹 Moving unused top-level files..."
mv -v engine.py "$TRASH" 2>/dev/null || true
mv -v pipeline.py "$TRASH" 2>/dev/null || true

echo "✅ Cleanup Wave 2 complete. Moved files to $TRASH"
