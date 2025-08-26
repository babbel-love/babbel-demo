#!/bin/bash
set -euo pipefail
echo "🧼 Babbel Local Safe Clean — No .trash_cleanup touched"

# Wipe known caches
rm -rf __pycache__/ core/__pycache__ || true

# Remove compiled files and obsolete CLI runner
rm -f test_pipeline_run.py chat.py.bak streamlit_babbel_app.py.bak || true

# Clean up deprecated duplicate core folder
rm -rf core || true

echo "✅ Core junk removed. .trash_cleanup untouched."
