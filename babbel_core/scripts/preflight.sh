#!/usr/bin/env bash
set -euo pipefail
ROOT="${BABBEL_CORE_ROOT:-babbel_core}"

echo "🔧 Preflight starting…"
python3 -V

echo "🔎 Byte-compile check…"
python3 -m compileall -q "$ROOT"

echo "🧪 Running unit tests…"
PYTHONPATH="." python3 -m unittest discover -v -s "$ROOT/tests" -t .

echo "🚀 Smoke run (orchestrator)…"
PYTHONPATH="." python3 - "$ROOT" <<'PY'
import os, json
from babbel_core.core.orchestrator import process_message
os.environ["BABBEL_CULTURE_SHIFT"] = "1"
os.environ["BABBEL_TARGET_CULTURE"] = "jp"
out = process_message("Quick test: I'm stressed and need one tiny step.")
print(json.dumps(out, indent=2)[:2000])  # truncate
PY

echo "✅ Preflight complete."
