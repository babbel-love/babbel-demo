from __future__ import annotations
from typing import Dict, Any
from .hx_engine import build_extras
from .culture_shift import apply_and_explain

def send(user_text: str = None, anchor: str = None, guiding_line: str = None, emotion: str = None, intent: str = None, show_metadata: bool = False) -> Dict[str, Any]:
    if not anchor or not isinstance(anchor, str):
        raise ValueError("anchor required")
    final_text, _ = apply_and_explain(user_text or "")
    extras = build_extras(final_text, emotion or "neutral", intent or "neutral", "neutral")
    return {
        "final_text": final_text,
        "ux": extras["ux"],
    }

def process_message(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("payload must be a dict")
    text = payload.get("text") or ""
    final_text, _ = apply_and_explain(text)
    extras = build_extras(final_text, payload.get("emotion", "neutral"), payload.get("intent", "neutral"), "neutral")
    payload["ux"] = extras["ux"]
    payload["final_text"] = final_text
    return payload
