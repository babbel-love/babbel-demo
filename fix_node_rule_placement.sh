#!/bin/bash
set -euo pipefail

FILE="babbel_core/node_rules.py"

echo "🔧 Fixing node rule placement for 'stuck' inside apply_node_rules..."

TMPFILE="$(mktemp)"
awk '
/def apply_node_rules/ {print; print "    if \"stuck\" in text.lower(): return \"Let’s take one small step together and see where it leads.\""; next}
{print}
' "$FILE" > "$TMPFILE"

mv "$TMPFILE" "$FILE"
echo "✅ Rule inserted inside apply_node_rules() properly."
