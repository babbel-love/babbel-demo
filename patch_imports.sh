#!/bin/bash
set -euo pipefail

APP="streamlit_babbel_app.py"

echo "🔧 Patching $APP with local path injection for imports..."

# Insert sys.path fix at the top
TMPFILE="$(mktemp)"
{
  echo 'import sys, os'
  echo 'sys.path.insert(0, os.path.dirname(__file__))  # Add local folder to import path'
  cat "$APP"
} > "$TMPFILE"

mv "$TMPFILE" "$APP"
chmod +x "$APP"

echo "✅ Patched: $APP now imports local modules correctly."
