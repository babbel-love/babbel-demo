#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
if [ -f requirements.txt ] && [ -s requirements.txt ]; then
  pip install -r requirements.txt
fi
python run.py
