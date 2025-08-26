import os, json, csv, time
from datetime import datetime
from typing import List, Dict, Any

CONV_DIR = os.path.join(os.getcwd(), "conversations")
EXPORT_DIR = os.path.join(os.getcwd(), "exports")
os.makedirs(CONV_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def autosave_session(name: str, data: Dict[str, Any]) -> str:
    path = os.path.join(CONV_DIR, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path

def load_session(name: str) -> Dict[str, Any]:
    path = os.path.join(CONV_DIR, f"{name}.json")
    if not os.path.exists(path): return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def export_history_csv(mode: str, history: List[Dict[str, Any]]) -> str:
    # history requires keys per spec; missing keys become empty
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(EXPORT_DIR, f"{mode}_history_{ts}.csv")
    fields = ["timestamp","mode","role","text","tone","emotion","intent","node","explanation","scoring"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in history:
            w.writerow({
                "timestamp": row.get("timestamp",""),
                "mode": mode,
                "role": row.get("role",""),
                "text": row.get("text",""),
                "tone": row.get("tone",""),
                "emotion": row.get("emotion",""),
                "intent": row.get("intent",""),
                "node": row.get("node",""),
                "explanation": row.get("explanation",""),
                "scoring": json.dumps(row.get("scoring",{}), ensure_ascii=False),
            })
    return path
