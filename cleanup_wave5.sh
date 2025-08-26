#!/bin/bash
set -e
TRASH=".trash_cleanup"
mkdir -p "$TRASH"

echo "🧹 Moving legacy or unused logic modules..."

mv -v babbel_core/cultural_shift_detector.py "$TRASH" 2>/dev/null || true
mv -v babbel_core/engine_patch.py "$TRASH" 2>/dev/null || true
mv -v babbel_core/hx_engine.py "$TRASH" 2>/dev/null || true
mv -v babbel_core/engine_memory.py "$TRASH" 2>/dev/null || true
mv -v babbel_core/tone_classifier.py "$TRASH" 2>/dev/null || true

echo "✅ Cleanup Wave 5 complete. You’re running lean now."
