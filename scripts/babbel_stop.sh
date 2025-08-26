#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PORT="${BABBEL_PORT:-8501}"
if [ -f .streamlit_pid ]; then
  PID="$(cat .streamlit_pid || true)"
  if [ -n "${PID:-}" ] && ps -p "$PID" > /dev/null 2>&1; then
    kill "$PID" || true
    sleep 1
    kill -9 "$PID" || true
  fi
  rm -f .streamlit_pid
fi
# Also free the port (safe kill: only Streamlit unless forced)
./scripts/free_port.sh "$PORT"
echo "Stopped."
