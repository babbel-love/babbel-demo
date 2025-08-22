#!/usr/bin/env bash
set -euo pipefail
PY="${PY:-python3}"
VENV="${VENV:-.venv}"
$PY -m venv "$VENV"
. "$VENV/bin/activate"
pip install --upgrade pip
if [ -f requirements.txt ]; then
  if [ -f constraints.txt ]; then
    pip install -r requirements.txt -c constraints.txt
  else
    pip install -r requirements.txt
  fi
fi
bash scripts/requirements_guard.sh
