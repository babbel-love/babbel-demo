import json, os
from datetime import datetime
from difflib import unified_diff

MEMORY_FILE = "memory_log.json"

def log_interaction(user_input, emotion, intent, raw_reply, final_reply, *,
                    node_nudge=None, rewrite_score=None, fact_flags=None):
    diff_lines = list(unified_diff(
        raw_reply.splitlines(), final_reply.splitlines(),
        fromfile='raw', tofile='final', lineterm=''
    ))
    log = {
        "timestamp": datetime.now().isoformat(),
        "input": user_input,
        "emotion": emotion,
        "intent": intent,
        "node_nudge": node_nudge,
        "rewrite_score": rewrite_score,
        "fact_flags": fact_flags or [],
        "raw_reply": raw_reply,
        "final_reply": final_reply,
        "rewrite_diff": diff_lines
    }

    existing = []
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []

    existing.append(log)

    with open(MEMORY_FILE, "w") as f:
        json.dump(existing[-100:], f, indent=2)

def get_recent_emotions(n=10):
    if not os.path.exists(MEMORY_FILE): return []
    with open(MEMORY_FILE, "r") as f:
        try:
            logs = json.load(f)
            return [entry["emotion"] for entry in logs[-n:] if "emotion" in entry]
        except:
            return []
