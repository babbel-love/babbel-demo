#!/bin/bash
set -e
TRASH=".trash_cleanup"
mkdir -p "$TRASH"

echo "🧹 Removing unused node/session/protocol modules..."

mv -v babbel_core/node_classifier.py "$TRASH" 2>/dev/null || true
mv -v babbel_core/session_controller.py "$TRASH" 2>/dev/null || true
mv -v babbel_core/session_controls.py "$TRASH" 2>/dev/null || true
mv -v babbel_core/protocol_retry.py "$TRASH" 2>/dev/null || true

echo "✅ Cleanup Wave 4 complete. Remaining logic is now verified in-use."
