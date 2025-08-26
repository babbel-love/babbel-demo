#!/bin/bash
set -euo pipefail

FILE="babbel_core/node_rules.py"

echo "🧹 Resetting and repairing broken top of node_rules.py..."

# Remove broken lines (early stuck insertions)
sed -i '' '/^if "stuck" in text.lower():/d' "$FILE"
sed -i '' '/Let’s take one small step/d' "$FILE"
sed -i '' '/^return "Let’s/d' "$FILE"

# Inject correct stuck rule inside the function
TMPFILE="$(mktemp)"
awk '
/def apply_node_rules\(text, emotion, intent\):/ {
  print
  print "    if \"stuck\" in text.lower(): return \"Let’s take one small step together and see where it leads.\""
  next
}
{ print }
' "$FILE" > "$TMPFILE"

mv "$TMPFILE" "$FILE"
echo "✅ node_rules.py is now clean and valid with 'stuck' rule injected."
