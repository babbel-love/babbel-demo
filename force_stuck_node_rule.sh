#!/bin/bash
set -euo pipefail

RULES="babbel_core/node_rules.py"
TMPFILE="$(mktemp)"

echo "🔧 Replacing node_rules.py with guaranteed valid version..."

cat <<'PY' > "$TMPFILE"
def apply_node_rules(text, emotion, intent):
    if "stuck" in text.lower():
        return "Let’s take one small step together and see where it leads."
    if emotion == "shame":
        return "You’re holding something unbearable — not because it’s true, but because it feels that way."
    elif emotion == "grief" and intent == "search for meaning":
        return "Grief isn’t just pain — it’s proof that something mattered. We’ll stay with that."
    elif emotion == "anger":
        return "That edge in your voice? It matters. Let’s hear it without trying to tame it."
    elif emotion == "wonder":
        return "There’s something alive in that wondering. Let’s not rush to explain it away."
    elif emotion == "fear" and intent == "seek guidance":
        return "I’m with you. We’ll face this carefully — not quickly."
    elif intent == "confession":
        return "You’re not asking for advice. You’re asking if it’s still okay to be seen. It is."
    else:
        return "Let’s slow this down together and see what’s really here."
PY

mv "$TMPFILE" "$RULES"
echo "✅ Rewritten node_rules.py — 'stuck' will now trigger node response."
