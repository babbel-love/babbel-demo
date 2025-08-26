#!/bin/bash
set -euo pipefail

echo "📁 Moving to Babbel_Builder_Tool..."
cd ~/Babbel_Builder_Tool

echo "🧹 Cleaning up Python caches..."
find . -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

echo "🚀 Launching Streamlit with correct PYTHONPATH..."
PYTHONPATH=babbel_official streamlit run babbel_official/babbel_core/streamlit_babbel_app.py
