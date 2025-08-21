#!/bin/bash
echo "🧪 Running full Babbel override integrity test suite..."
source .venv/bin/activate
./scripts/scan_override.sh || exit 1
pytest tests/ --tb=short -q || exit 1
echo "✅ All integrity checks passed."
