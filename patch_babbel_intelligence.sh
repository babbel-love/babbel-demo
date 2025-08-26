#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo "🔧 Patching Babbel intelligence core..."

# === memory_tracker.py ===
cat <<'PY' > babbel_core/memory_tracker.py
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
PY

# === test_overlays.py ===
mkdir -p babbel_core/tests
cat <<'PY' > babbel_core/tests/test_overlays.py
import json

def test_babbel_metadata_complete():
    with open("memory_log.json") as f:
        logs = json.load(f)
    assert len(logs) > 0
    for entry in logs:
        assert "emotion" in entry
        assert "intent" in entry
        assert "node_nudge" in entry
        assert "rewrite_score" in entry
        assert isinstance(entry["rewrite_score"], (int, float))
        assert "final_reply" in entry
        assert entry["final_reply"].strip() != entry["raw_reply"].strip()
PY

# === schema validation integration example ===
cat <<'PY' > babbel_core/schema_validation.py
from pydantic import BaseModel

class FinalOutputSchema(BaseModel):
    final_text: str
    tokens_used: int
    summary: str

def validate_final_output(data: dict) -> FinalOutputSchema:
    return FinalOutputSchema(**data)
PY

echo "✅ Patch complete. You can now:"
echo " - Log all metadata (emotion, intent, node, score, diff)"
echo " - Export full logs via Streamlit"
echo " - Run: pytest -q babbel_core/tests/"
