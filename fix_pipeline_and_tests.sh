#!/bin/bash

set -e

echo "🔧 Fixing circular imports and test imports..."

# Step 1: Fix internal imports inside core/pipeline.py
sed -i '' \
  -e 's/from babbel_core\.core import review/from . import review/' \
  -e 's/from babbel_core\.core import intent_classifier/from . import intent_classifier/' \
  -e 's/from babbel_core\.core import emotion_classifier/from . import emotion_classifier/' \
  -e 's/from babbel_core\.core import tone_constants/from . import tone_constants/' \
  babbel_core/core/pipeline.py

# Step 2: Fix incorrect test imports of run_pipeline
find babbel_core/tests -type f -name "*.py" -exec sed -i '' \
  -e 's/from babbel_core\.pipeline/from babbel_core.core.pipeline/' {} +

echo "✅ Imports patched. Re-run tests with:"
echo "    pytest babbel_core/tests --tb=short -q"
