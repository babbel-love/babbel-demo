import os
import json

def load_history(session_id='default') -> list[str]:
    path = f".memory_{session_id}.json"
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []
