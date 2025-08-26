#!/bin/bash
set -euo pipefail

mkdir -p babbel_core/sessions
touch babbel_core/__init__.py

echo "✅ Memory expansion structure ready:"
tree -L 2 babbel_core
