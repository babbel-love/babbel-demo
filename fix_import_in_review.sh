#!/bin/bash
cd "$(git rev-parse --show-toplevel || pwd)"

# Fix import in review.py to be relative
cat <<'PY' > babbel_core/review.py
from .rewrite import rewrite_tone, enforce_babbel_style

def run_review_stage(draft: str) -> dict:
    toned = rewrite_tone(draft)
    styled = enforce_babbel_style(toned)
    return {
        "reviewed_text": styled,
        "quick_check": "Tone strengthened. Style rewritten to match Babbel voice."
    }
PY

echo "✅ Fixed relative import in review.py"
