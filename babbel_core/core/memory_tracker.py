from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from .config import load

def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def log_interaction(emotion: str, intent: str, user_input: str, response: str) -> None:
    cfg = load()
    p = Path(cfg.MEMORY_FILE)
    data = []
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            data = []
    data.append({
        "ts": _now_utc_iso(),
        "emotion": emotion,
        "intent": intent,
        "user_input": user_input,
        "response": response
    })
    p.write_text(json.dumps(data[-100:], ensure_ascii=False, indent=2), encoding="utf-8")
