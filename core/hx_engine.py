from __future__ import annotations
from typing import Dict, Any
from .schema import standard_payload, UXBlock
from .culture_shift import apply_and_explain

def build_extras(final_text: str, emotion: str, intent: str, tone: str) -> Dict[str, Any]:
    thoughts = f"reflection: consider emotional impact of: {final_text[:120]}"
    ux = UXBlock(
        thoughts=thoughts,
        reflection="reflection",
        tips="clarify or soften as needed",
    )
    return {
        "ux": ux.to_dict(),
        "emotion": emotion,
        "intent": intent,
        "tone": tone,
    }
