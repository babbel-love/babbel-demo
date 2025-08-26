#!/bin/bash
set -euo pipefail

echo "🔧 Fixing scoring import in pipeline.py..."

sed -i '' 's/from rewrite_scoring /from babbel_core.rewrite_scoring /' babbel_core/pipeline.py

echo "✅ Done. Re-run with: pytest -q babbel_core/tests"
