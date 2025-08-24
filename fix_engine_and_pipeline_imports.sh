#!/bin/bash

set -e
echo "🔧 Fixing engine.py and pipeline.py import paths..."

# Fix prompt_builder in engine.py
sed -i '' 's|from babbel_core\.core\.prompt_builder|from babbel_core.prompt_builder|' babbel_core/engine.py

# Fix schema import in pipeline.py
sed -i '' 's|from \.\.schema|from .schema|' babbel_core/core/pipeline.py

echo "✅ Imports fixed."
echo "🧪 Now run: pytest babbel_core/tests --tb=short -q"
