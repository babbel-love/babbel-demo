#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
mkdir -p babbel_core/tests

echo "🔧 Installing all 7 Babbel tests..."

# === 1. test_pipeline.py ===
cat <<'PY' > babbel_core/tests/test_pipeline.py
from pipeline import run_pipeline

def test_pipeline_response():
    out = run_pipeline("I feel ashamed and want to disappear.")
    assert "you’re holding something unbearable" in out.lower()
    assert "babbel voice" in out.lower()
    assert "fact" in out.lower()
PY

# === 2. test_node_rules.py ===
cat <<'PY' > babbel_core/tests/test_node_rules.py
from node_rules import apply_node_rules

def test_node_shame_confession():
    msg = "I feel disgusting and I know it’s my fault"
    out = apply_node_rules(msg, "shame", "confession")
    assert "not because it’s true" in out.lower()

def test_node_grief_search():
    msg = "Why does it hurt so much?"
    out = apply_node_rules(msg, "grief", "search for meaning")
    assert "proof that something mattered" in out.lower()
PY

# === 3. test_emotion_classifier.py ===
cat <<'PY' > babbel_core/tests/test_emotion_classifier.py
from emotion_classifier import classify_emotion

def test_detect_shame():
    assert classify_emotion("I feel ashamed and disgusting") == "shame"

def test_detect_wonder():
    assert classify_emotion("What if I did something bold?") == "wonder"
PY

# === 4. test_intent_classifier.py ===
cat <<'PY' > babbel_core/tests/test_intent_classifier.py
from intent_classifier import classify_intent

def test_confession_detect():
    assert classify_intent("I’m sorry, it’s my fault") == "confession"

def test_protest_detect():
    assert classify_intent("You always do this to me") == "protest"
PY

# === 5. test_overlays.py ===
cat <<'PY' > babbel_core/tests/test_overlays.py
import json

def test_babbel_metadata_complete():
    with open("memory_log.json") as f:
        logs = json.load(f)
    assert logs, "No logs found"
    for entry in logs:
        assert all(k in entry for k in ("emotion", "intent", "node_nudge", "rewrite_score"))
        assert entry["final_reply"].strip() != entry["raw_reply"].strip()
PY

# === 6. test_rewrite.py ===
cat <<'PY' > babbel_core/tests/test_rewrite.py
from rewrite import rewrite_tone, enforce_babbel_style

def test_rewrite_tone_removes_hedges():
    text = "I just think maybe we could try."
    out = rewrite_tone(text)
    assert "just" not in out.lower()
    assert "maybe" not in out.lower()

def test_babbel_style_strengthens_phrases():
    text = "It is important to note that we should utilize time."
    out = enforce_babbel_style(text)
    assert "important to note" not in out.lower()
    assert "utilize" not in out.lower()
    assert "should" not in out.lower()
PY

# === 7. test_review.py ===
cat <<'PY' > babbel_core/tests/test_review.py
from review import run_review_stage

def test_review_response():
    result = run_review_stage("This might help, perhaps.")
    assert isinstance(result, dict)
    assert "reviewed_text" in result
    assert "babbel" in result["quick_check"].lower()
PY

echo "✅ All 7 tests installed. Run:"
echo "   pytest -q babbel_core/tests"
