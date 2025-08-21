from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

# Common emotion aliases normalized for downstream logic.
ALIASES = {
    "rage": "anger",
    "mad": "anger",
    "sadness": "grief",
    "sad": "grief",
    "mourning": "grief",
    "awe": "wonder",
    "surprise": "wonder",
    "guilt": "shame",
    "embarrassment": "shame",
    "anxious": "fear",
    "anxiety": "fear",
}

@dataclass
class FinalPayload:
    trace_id: str
    guiding_line: str
    final_text: str
    emotion: str
    intent: str
    notes: Optional[str]
    tokens_used: Optional[int]
    timestamp_utc: str
    safety: Dict[str, Any]
    ux: Optional[Dict[str, Any]] = None  # NEW: UX block for GUI

def _is_utc_iso(s: str) -> bool:
    try:
        if s.endswith("Z"):
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(s)
        return (dt.tzinfo is not None) and (dt.utcoffset() == timedelta(0))
    except Exception:
        return False

def validate_payload(obj: dict) -> FinalPayload:
    required = ["trace_id", "guiding_line", "final_text", "emotion", "intent", "timestamp_utc", "safety"]
    for k in required:
        if k not in obj:
            raise ValueError(f"missing field: {k}")
    guiding_line = str(obj["guiding_line"]).strip()
    final_text = str(obj["final_text"]).strip()
    if not guiding_line or not final_text:
        raise ValueError("guiding_line and final_text must be non-empty")
    emotion = ALIASES.get(str(obj["emotion"]).lower(), str(obj["emotion"]).lower())
    intent = str(obj["intent"]).lower()
    if not _is_utc_iso(str(obj["timestamp_utc"])):
        raise ValueError("timestamp_utc must be UTC ISO 8601")
    safety = obj["safety"]
    if not (
        isinstance(safety, dict)
        and "blocked" in safety
        and "reasons" in safety
        and isinstance(safety["blocked"], bool)
        and isinstance(safety["reasons"], list)
    ):
        raise ValueError("invalid safety shape")
    ux = obj.get("ux")
    if ux is not None and not isinstance(ux, dict):
        raise ValueError("ux must be a dict or omitted")
    tok = obj.get("tokens_used")
    if tok is not None and not isinstance(tok, int):
        raise ValueError("tokens_used must be int or omitted")
    return FinalPayload(
        trace_id=str(obj["trace_id"]),
        guiding_line=guiding_line,
        final_text=final_text,
        emotion=emotion,
        intent=intent,
        notes=obj.get("notes"),
        tokens_used=tok,
        timestamp_utc=str(obj["timestamp_utc"]),
        safety=safety,
        ux=ux,
    )

def to_dict(fp: FinalPayload) -> dict:
    out = {
        "trace_id": fp.trace_id,
        "guiding_line": fp.guiding_line,
        "final_text": fp.final_text,
        "emotion": fp.emotion,
        "intent": fp.intent,
        "notes": fp.notes,
        "tokens_used": fp.tokens_used,
        "timestamp_utc": fp.timestamp_utc,
        "safety": fp.safety,
    }
    if fp.ux is not None:
        out["ux"] = fp.ux
    return out
