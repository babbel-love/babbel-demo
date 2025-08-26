#!/bin/bash
set -euo pipefail

PIPELINE="babbel_core/pipeline.py"
TMPFILE="$(mktemp)"

echo "🔧 Patching run_pipeline() to enforce Babbel node-based rewrite..."

awk '
BEGIN {patched = 0}
/def run_pipeline\(prompt: str\):/ {
  print
  print "    from babbel_core.emotion_classifier import classify_emotion"
  print "    from babbel_core.intent_classifier import classify_intent"
  print "    from babbel_core.node_rules import apply_node_rules"
  next
}
{
  print
  if (!patched && /# Final answer/) {
    patched = 1
    print ""
    print "    # 🧠 Babbel node-based rewrite enforcement"
    print "    emotion = classify_emotion(prompt)"
    print "    intent = classify_intent(prompt)"
    print "    node_out = apply_node_rules(prompt, emotion, intent)"
    print "    if node_out != \"Let’s slow this down together and see what’s really here.\":" 
    print "        prompt = node_out"
  }
}
' "$PIPELINE" > "$TMPFILE"

mv "$TMPFILE" "$PIPELINE"

echo "✅ Node override is now enforced in run_pipeline()."
