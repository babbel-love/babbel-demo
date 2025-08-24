#!/usr/bin/env bash
set -euo pipefail
bash scripts/deny_scan.sh
pytest -q
python -m streamlit run streamlit_babbel_app.py
