#!/bin/bash
set -euo pipefail

FILE="babbel_core/pipeline.py"
TMPFILE="$(mktemp)"

echo "🔧 Overwriting run_pipeline() to use node output directly..."

awk '
BEGIN {inside = 0}
/def run_pipeline\(prompt: str\):/ {
  print
  print "    from babbel_core.intent_classifier import classify_intent"
  print "    from babbel_core.emotion_classifier import classify_emotion"
  print "    from babbel_core.node_rules import apply_node_rules"
  inside = 1
  next
}
inside && /final_text = / {
  print ""
  print "    # Node rewrite block"
  print "    emotion = classify_emotion(prompt)"
  print "    intent = classify_intent(prompt)"
  print "    node_out = apply_node_rules(prompt, emotion, intent)"
  print "    final_text = enforce_babbel_style(rewrite_tone(node_out)).strip()"
  next
}
{ print }
' "$FILE" > "$TMPFILE"

mv "$TMPFILE" "$FILE"
echo "✅ run_pipeline() now uses full Babbel node output as the response."
