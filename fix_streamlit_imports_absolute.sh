#!/bin/bash
set -euo pipefail

FILE="babbel_core/streamlit_babbel_app.py"

echo "🔧 Patching $FILE for Streamlit compatibility..."

sed -i '' 's/from \.pipeline /from babbel_core.pipeline /' "$FILE"
sed -i '' 's/from \.thread /from babbel_core.thread /' "$FILE"
sed -i '' 's/from \.memory_tracker /from babbel_core.memory_tracker /' "$FILE"

echo "✅ Patched to use absolute imports."
