#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PORT="${BABBEL_PORT:-8501}"

# Stop any previous instances and free the port
./scripts/babbel_stop.sh || true
./scripts/free_port.sh "$PORT"

: > streamlit.out
nohup python -m streamlit run "babbel_core/streamlit_babbel_app.py" --server.port "$PORT" >> streamlit.out 2>&1 &
echo $! > .streamlit_pid
echo "Started Streamlit on http://localhost:${PORT} (PID $(cat .streamlit_pid))"
