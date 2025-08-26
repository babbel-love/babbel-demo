#!/usr/bin/env bash
set -euo pipefail
for f in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.bash_profile"; do
  [ -f "$f" ] || continue
  cp "$f" "$f.bak.$(date +%s)"
  # Drop any PYTHONWARNINGS lines (common culprit for "Invalid -W option")
  sed -i '' '/PYTHONWARNINGS/d' "$f" || true
done
unset PYTHONWARNINGS || true
echo "✅ Cleaned PYTHONWARNINGS. Open a new terminal window to load changes."
