#!/usr/bin/env bash
set -euo pipefail
: "${OPENROUTER_API_KEY:?Missing OPENROUTER_API_KEY}"
: "${OPENROUTER_SITE_URL:=http://localhost:8501}"
: "${OPENROUTER_APP_TITLE:=Babbel Official Dev}"
export NO_PROXY="localhost,127.0.0.1"
unset PYTHONWARNINGS || true
exec python3 -E -W ignore -m streamlit run "babbel_core/streamlit_babbel_app.py" --server.address=localhost --server.port=8501
