#!/bin/bash
set -euo pipefail

APP="streamlit_babbel_app.py"
TMPFILE="$(mktemp)"

echo "🔧 Enforcing full Babbel override in runtime..."

awk '
BEGIN {injection = 0}
/# assistant turn/ {injection = 1}
{
  print
  if (injection && /st\.chat_message\("assistant"\)/) {
    injection = 0
    print "        # 🔒 Force full Babbel rewrite, always"
    print "        from babbel_core.emotion_classifier import classify_emotion"
    print "        from babbel_core.intent_classifier import classify_intent"
    print "        from babbel_core.node_rules import apply_node_rules"
    print "        from babbel_core.rewrite import rewrite_tone, enforce_babbel_style"
    print "        emo = classify_emotion(prompt)"
    print "        intent = classify_intent(prompt)"
    print "        node_out = apply_node_rules(prompt, emo, intent)"
    print "        assistant_text = enforce_babbel_style(rewrite_tone(node_out)).strip()"
  }
}
' "$APP" > "$TMPFILE"

mv "$TMPFILE" "$APP"
echo "✅ Babbel override active — model output will never appear unfiltered."
