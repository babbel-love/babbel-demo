#!/bin/bash

set -e
echo "🔧 Fixing all pipeline and schema import paths..."

# Fix schema import inside pipeline.py
sed -i '' 's|from \.\.schema|from .schema|' babbel_core/core/pipeline.py

# Fix pipeline import inside engine.py
sed -i '' 's|from babbel_core\.pipeline|from babbel_core.core.pipeline|' babbel_core/engine.py

# Fix test files that import babbel_core.pipeline (should point to core.pipeline)
find babbel_core/tests -type f -name "*.py" -exec sed -i '' \
  -e 's|from babbel_core\.pipeline|from babbel_core.core.pipeline|' \
  {} +

echo "✅ All pipeline and schema import paths are now fixed."
echo "🧪 You can now run:"
echo "    pytest babbel_core/tests --tb=short -q"
