#!/bin/bash

set -e

echo "🔧 Updating __init__.py and patching test imports..."

# Step 1: Rebuild __init__.py exports from the new full logic set
cat <<'PY' > babbel_core/core/__init__.py
from .pipeline import run_pipeline
from .rewrite import rewrite_tone, enforce_babbel_style, rewrite_response
from .memory_tracker import log_interaction, get_recent_emotions
from .node_rules import apply_node_rules
from .classifier import classify_emotion, classify_intent
from .style_engine import *
from .schema import validate_final_output
from .safety import *
from .tokens import *
from .orchestrator import *
from .observability import *
from .culture_shift import *
from .fallback import *
from .hx_engine import *
PY

# Step 2: Patch known broken imports in tests
find babbel_core/tests -type f -name "*.py" -exec sed -i '' \
  -e 's/from babbel_core\.core\.prompt_builder/from babbel_core.core.pipeline/' \
  -e 's/from babbel_core\.core\.review/from babbel_core.core.rewrite/' {} +

# Step 3: Confirm
echo "✅ Babbel core/__init__.py exports reset."
echo "✅ Test import paths patched (prompt_builder → pipeline, review → rewrite)."
echo ""
echo "🧪 You can now run:"
echo "    pytest babbel_core/tests --tb=short -q"
echo ""

