from __future__ import annotations
from typing import Tuple

def apply_node_rules(text: str, emotion: str, intent: str) -> Tuple[str, str]:
    # guiding_line describes why the shaping happened
    if emotion == "shame":
        return "You’re holding something unbearable — not because it’s true, but because it feels that way.", "Name and validate shame before action."
    elif emotion == "grief" and intent == "search for meaning":
        return "Grief isn’t just pain — it’s proof that something mattered. We’ll stay with that.", "Honor grief; avoid premature meaning-making."
    elif emotion == "anger":
        return "That edge in your voice? It matters. Let’s hear it without trying to tame it.", "Allow anger; channel without suppression."
    elif emotion == "wonder":
        return "There’s something alive in that wondering. Let’s not rush to explain it away.", "Protect curiosity; avoid over-explaining."
    elif emotion == "fear" and intent == "seek guidance":
        return "I’m with you. We’ll face this carefully — not quickly.", "Safety-first pacing."
    elif intent == "confession":
        return "You’re not asking for advice. You’re asking if it’s still okay to be seen. It is.", "Witness confession; reduce moralizing."
    else:
        return "Let’s slow this down together and see what’s really here.", "Default: slow and see."
