#!/bin/bash
set -euo pipefail

echo "📦 Converting Babbel_Official to a proper Python module: babbel_core/..."

mkdir -p babbel_core

# Move logic files to module folder
mv rewrite.py rewrite_scoring.py pipeline.py emotion_classifier.py intent_classifier.py node_rules.py memory_tracker.py babbel_core/

# Add __init__.py
touch babbel_core/__init__.py

# Patch streamlit_babbel_app.py imports
TMPFILE="$(mktemp)"
sed \
  -e 's/from rewrite /from babbel_core.rewrite /' \
  -e 's/from rewrite_scoring /from babbel_core.rewrite_scoring /' \
  -e 's/from emotion_classifier /from babbel_core.emotion_classifier /' \
  -e 's/from intent_classifier /from babbel_core.intent_classifier /' \
  -e 's/from node_rules /from babbel_core.node_rules /' \
  -e 's/from memory_tracker /from babbel_core.memory_tracker /' \
  streamlit_babbel_app.py > "$TMPFILE"

mv "$TMPFILE" streamlit_babbel_app.py

echo "✅ Project is now a real module: babbel_core/"
echo "✅ Patched streamlit_babbel_app.py to import from babbel_core"

echo
echo "🚀 Run it with:"
echo "  streamlit run streamlit_babbel_app.py"
