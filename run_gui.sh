#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
PYTHONPATH=".:$PYTHONPATH" python3 -m babbel_gui.app
