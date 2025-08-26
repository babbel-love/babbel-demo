#!/bin/bash

set -e

echo "🔧 Restructuring babbel_core folder (rewrite.py already in core)..."

# Step 1: Ensure core/ exists
mkdir -p babbel_core/core

# Step 2: Move logic files (skip rewrite.py — already inside core/)
mv babbel_core/pipeline.py babbel_core/core/pipeline.py
mv babbel_core/review.py babbel_core/core/review.py
mv babbel_core/schema_validation.py babbel_core/core/schema_validation.py
mv babbel_core/memory_tracker.py babbel_core/core/memory_tracker.py
mv babbel_core/emotion_classifier.py babbel_core/core/emotion_classifier.py
mv babbel_core/intent_classifier.py babbel_core/core/intent_classifier.py
mv babbel_core/node_rules.py babbel_core/core/node_rules.py
mv babbel_core/node_rewrite_v2.py babbel_core/core/node_rewrite_v2.py

# Step 3: Create __init__.py files if missing
touch babbel_core/__init__.py
touch babbel_core/core/__init__.py

# Step 4: Patch core/__init__.py with module exports
cat <<'PY' > babbel_core/core/__init__.py
from .pipeline import run_pipeline
from .rewrite import rewrite_tone, enforce_babbel_style
from .review import run_review_stage
from .schema_validation import validate_final_output
from .emotion_classifier import classify_emotion
from .intent_classifier import classify_intent
from .node_rules import apply_node_rules
from .node_rewrite_v2 import NodeRewriterV2
from .memory_tracker import log_interaction, get_recent_emotions
PY

# Step 5: Patch test imports
if [ -f "babbel_core/tests/test_engine.py" ]; then
  sed -i '' 's/from babbel_core\.core\.prompt_builder/from babbel_core.core.pipeline/' babbel_core/tests/test_engine.py
fi

if [ -f "babbel_core/tests/test_review.py" ]; then
  sed -i '' 's/from babbel_core\.core\.review/from babbel_core.core.review/' babbel_core/tests/test_review.py
fi

# Step 6: Confirm
echo "✅ Babbel Core structure fixed."
echo "Run tests with:"
echo "    pytest babbel_core/tests --tb=short -q"
echo ""

