#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python scripts/seed_sessions.py || true
python scripts/print_tree.py || true
python -m streamlit run streamlit_babbel_app.py
