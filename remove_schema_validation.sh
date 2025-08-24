#!/bin/bash

set -e

echo "🧹 Removing old schema_validation.py and fixing imports..."

# Step 1: Delete old file if it exists
rm -f babbel_core/schema_validation.py

# Step 2: Replace imports across codebase
find babbel_core -type f -name "*.py" -exec sed -i '' \
  -e 's/from babbel_core\.schema_validation/from babbel_core.core.schema/' \
  -e 's/import babbel_core\.schema_validation/import babbel_core.core.schema/' \
  {} +

echo "✅ Old schema_validation.py removed."
echo "✅ All imports now point to babbel_core.core.schema"
