#!/bin/bash
set -euo pipefail

echo "🔧 Patching broken test imports..."

# Fix imports in test_pipeline.py
sed -i '' 's/from rewrite /from babbel_core.rewrite /' babbel_core/tests/test_pipeline.py

# Fix imports in test_engine.py
sed -i '' 's/from engine /from babbel_core.engine /' babbel_core/tests/test_engine.py

# Add missing run_node_rewrite if not present
REWRITE_PATH="babbel_core/node_rewrite_v2.py"
if ! grep -q 'def run_node_rewrite' "$REWRITE_PATH"; then
cat <<'EOF' >> "$REWRITE_PATH"

def run_node_rewrite(text: str) -> str:
    rewriter = NodeRewriterV2()
    return rewriter.rewrite_node(text)
EOF
fi

echo "✅ Tests patched. Re-run with: pytest -q babbel_core/tests"
