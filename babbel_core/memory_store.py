import json, os, time
from typing import Any, Dict, List

ROOT = os.path.expanduser("~/.babbel/memory")
os.makedirs(ROOT, exist_ok=True)

def _path(session_id: str) -> str:
    return os.path.join(ROOT, f"{session_id}.json")

def load(session_id: str) -> Dict[str, Any]:
    p = _path(session_id)
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"session_id": session_id, "created_at": time.time(), "messages": []}

def append(session_id: str, role: str, content: str, meta: Dict[str, Any] = None) -> Dict[str, Any]:
    doc = load(session_id)
    doc["messages"].append({
        "ts": time.time(),
        "role": role,
        "content": content,
        "meta": meta or {}
    })
    tmp = _path(session_id) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    os.replace(tmp, _path(session_id))
    return doc
