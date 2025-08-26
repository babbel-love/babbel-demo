#!/bin/bash
set -euo pipefail

FILE="babbel_core/streamlit_babbel_app.py"

echo "🔧 Fixing imports in $FILE..."
sed -i '' 's/from pipeline /from .pipeline /' "$FILE"
sed -i '' 's/from thread /from .thread /' "$FILE"
sed -i '' 's/from memory_tracker /from .memory_tracker /' "$FILE"

echo "✅ Imports patched."
