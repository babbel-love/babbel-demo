# babbel_core/memory_tracker.py
import json, os
from datetime import datetime

MEMORY_FILE = "memory_log.json"

def log_interaction(user_input, emotion, intent, raw_reply, final_reply):
    log = {
        "timestamp": datetime.now().isoformat(),
        "input": user_input,
        "emotion": emotion,
        "intent": intent,
        "raw_reply": raw_reply,
        "final_reply": final_reply
    }
    existing = []
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = []
    existing.append(log)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(existing[-100:], f, ensure_ascii=False, indent=2)

def get_recent_emotions(n=10):
    if not os.path.exists(MEMORY_FILE): return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
            return [entry.get("emotion","") for entry in logs[-n:]]
    except Exception:
        return []
