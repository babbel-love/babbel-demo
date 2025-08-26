#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PORT="${BABBEL_PORT:-8501}"
if [ -f .streamlit_pid ]; then
  PID="$(cat .streamlit_pid || true)"
  if [ -n "${PID:-}" ] && ps -p "$PID" > /dev/null 2>&1; then
    echo "Running: PID $PID on port $PORT"
    exit 0
  fi
fi
if lsof -ti tcp:"$PORT" >/dev/null 2>&1; then
  echo "A process is listening on port $PORT (not tracked by .streamlit_pid)."
  exit 0
fi
echo "Not running."
exit 1
