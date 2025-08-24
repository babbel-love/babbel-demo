from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any

def get_recent(n: int, memory_file: str) -> List[Dict[str, Any]]:
    p = Path(memory_file)
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        rows = data[-max(0, int(n)):] 
        out = []
        for r in rows:
            out.append({
                "ts": r.get("ts") or r.get("timestamp"),
                "emotion": r.get("emotion",""),
                "intent": r.get("intent",""),
                "user_input": r.get("user_input") or r.get("input") or "",
                "response": r.get("response") or r.get("final_reply") or "",
            })
        return out
    except Exception:
        return []
