#!/bin/bash
echo "🔁 Rebuilding Babbel environment..."
rm -rf .venv __pycache__ .pytest_cache *.egg-info dist build
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Environment rebuilt and dependencies installed."
