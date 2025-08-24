from pathlib import Path
import os

SESS_DIR = "saved_sessions"

try:
    idx = os.path.join(SESS_DIR, "index.json")
    # placeholder logic — replace with real index handling if needed
except Exception as e:
    print(f"⚠️ Error loading index: {e}")
