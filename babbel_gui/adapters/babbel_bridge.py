from __future__ import annotations
from typing import Any, Dict

def get_babbel_response(text: str) -> Dict[str, Any]:
    try:
        from babbel.orchestrator import process_message
        out = process_message(text)
    except Exception:
        return {
            "reply_text": "(Babbel) I’m here. Tell me what you need.",
            "metadata": {"emotion":"calm","intent":"assist","tone":"supportive","node":"Embodied Agency"},
            "emotion_bar": [0.2]*16, "scores": {"coherence":0.9}
        }
    reply = out.get("final_text") or out.get("reply_text") or out.get("text") or str(out)
    meta = out.get("metadata") or {}
    for k in ("emotion","tone","intent","node"):
        if k in out: meta.setdefault(k, out[k])
    ebar = out.get("emotion_bar") or [0.25]*16
    scores = out.get("scores") or {}
    return {"reply_text": reply, "metadata": meta, "emotion_bar": ebar, "scores": scores}
