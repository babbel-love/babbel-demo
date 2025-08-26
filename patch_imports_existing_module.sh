#!/bin/bash
set -euo pipefail

echo "🔧 Patching streamlit_babbel_app.py to use babbel_core imports..."

APP="streamlit_babbel_app.py"
TMPFILE="$(mktemp)"

sed \
  -e 's/from rewrite /from babbel_core.rewrite /' \
  -e 's/from rewrite_scoring /from babbel_core.rewrite_scoring /' \
  -e 's/from emotion_classifier /from babbel_core.emotion_classifier /' \
  -e 's/from intent_classifier /from babbel_core.intent_classifier /' \
  -e 's/from node_rules /from babbel_core.node_rules /' \
  -e 's/from memory_tracker /from babbel_core.memory_tracker /' \
  "$APP" > "$TMPFILE"

mv "$TMPFILE" "$APP"

echo "✅ Patched all imports to reference babbel_core."
