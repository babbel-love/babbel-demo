#!/bin/bash
set -euo pipefail

echo "🔧 Patching all core modules for relative imports..."

FILES=$(find babbel_core -type f -name "*.py")

for f in $FILES; do
  sed -i '' 's/^from rewrite /from .rewrite /' "$f"
  sed -i '' 's/^from thread /from .thread /' "$f"
  sed -i '' 's/^from memory_tracker /from .memory_tracker /' "$f"
  sed -i '' 's/^from emotion_classifier /from .emotion_classifier /' "$f"
  sed -i '' 's/^from intent_classifier /from .intent_classifier /' "$f"
  sed -i '' 's/^from node_rewrite_v2 /from .node_rewrite_v2 /' "$f"
  sed -i '' 's/^from node_rules /from .node_rules /' "$f"
  sed -i '' 's/^from schema_validation /from .schema_validation /' "$f"
done

echo "✅ All relative imports patched."
