import json, os
from datetime import datetime
MEMORY_FILE = "memory_log.json"

def log_interaction(user_input, emotion, intent, raw_reply, final_reply, session_id: str = ""):
    log = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id or "",
        "input": user_input,
        "emotion": emotion,
        "intent": intent,
        "raw_reply": raw_reply,
        "final_reply": final_reply
    }
    existing = []
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
    existing.append(log)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(existing[-100:], f, ensure_ascii=False, indent=2)

def get_recent_emotions(n=10):
    if not os.path.exists(MEMORY_FILE): 
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        try:
            logs = json.load(f)
            return [entry.get("emotion","") for entry in logs[-n:] if "emotion" in entry]
        except Exception:
            return []
