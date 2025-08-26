#!/bin/bash
set -euo pipefail

RULES="babbel_core/node_rules.py"

if ! grep -q '"stuck"' "$RULES"; then
  echo "🔧 Injecting rewrite rule for 'I feel stuck'..."
  sed -i '' '2i\
if "stuck" in text.lower():\
    return "Let’s take one small step together and see where it leads."
' "$RULES"
else
  echo "✅ Rule for 'stuck' already exists."
fi
