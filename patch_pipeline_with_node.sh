#!/bin/bash
set -euo pipefail

echo "🔧 Upgrading run_pipeline() to apply node-based rewrites..."

PIPELINE="babbel_core/pipeline.py"
TMPFILE="$(mktemp)"

awk '
BEGIN {
  inserted = 0
}
{
  print
  if (!inserted && /def run_pipeline\(prompt: str\):/) {
    inserted = 1
    print "    from babbel_core.intent_classifier import classify_intent"
    print "    from babbel_core.emotion_classifier import classify_emotion"
    print "    from babbel_core.node_rules import apply_node_rules"
  }

  if ($0 ~ /# Final answer/) {
    print ""
    print "    # Node-based rewrite"
    print "    emotion = classify_emotion(prompt)"
    print "    intent = classify_intent(prompt)"
    print "    node_response = apply_node_rules(prompt, emotion, intent)"
    print "    prompt = node_response  # override input with node-guided message"
  }
}
' "$PIPELINE" > "$TMPFILE"

mv "$TMPFILE" "$PIPELINE"
echo "✅ Babbel pipeline now applies node rewrites automatically."
