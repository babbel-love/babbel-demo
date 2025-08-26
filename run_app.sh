#!/usr/bin/env bash
set -euo pipefail
export PYTHONUNBUFFERED=1
exec python -m streamlit run streamlit_babbel_app.py
