#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/healthcheck.py
./scripts/babbel_stop.sh || true
./scripts/babbel_start.sh
sleep 2
python scripts/healthcheck.py
echo "[SMOKE] Last 100 lines of streamlit.out:"
tail -n 100 streamlit.out || true
