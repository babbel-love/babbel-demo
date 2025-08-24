from __future__ import annotations
from typing import Tuple

def apply_node_rules(text: str, emotion: str, intent: str) -> Tuple[str, str]:
    # guiding_line describes why the shaping happened; we do not alter `text` here.
    if emotion == "shame":
        return text, "You’re holding something unbearable — not because it’s true, but because it feels that way."
    elif emotion == "grief" and intent == "search for meaning":
        return text, "Grief isn’t just pain — it’s proof that something mattered. We’ll stay with that."
    elif emotion == "anger":
        return text, "That edge in your voice? It matters. Let’s hear it without trying to tame it."
    elif emotion == "wonder":
        return text, "There’s something alive in that wondering. Let’s not rush to explain it away."
    elif emotion == "fear" and intent == "seek guidance":
        return text, "I’m with you. We’ll face this carefully — not quickly."
    elif intent == "confession":
        return text, "You’re not asking for advice. You’re asking if it’s still okay to be seen. It is."
    else:
        return text, "Let’s slow this down together and see what’s really here."
