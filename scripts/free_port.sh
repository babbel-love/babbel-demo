#!/usr/bin/env bash
set -euo pipefail
PORT="${1:-8501}"
FORCE="${BABBEL_FORCE_PORT:-0}"
PIDS="$(lsof -ti tcp:"$PORT" || true)"
[ -z "$PIDS" ] && exit 0
echo "Port $PORT in use by: $PIDS"
for pid in $PIDS; do
  cmd="$(ps -p "$pid" -o comm= || true)"
  if echo "$cmd" | grep -qi 'streamlit'; then
    echo "Killing Streamlit PID $pid"
    kill "$pid" || true; sleep 1; kill -9 "$pid" || true
  else
    if [ "$FORCE" = "1" ]; then
      echo "FORCE kill PID $pid (cmd=$cmd)"
      kill "$pid" || true; sleep 1; kill -9 "$pid" || true
    else
      echo "Skipping non-Streamlit PID $pid (cmd=$cmd). Set BABBEL_FORCE_PORT=1 to force."
    fi
  fi
done
