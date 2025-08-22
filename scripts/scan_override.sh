#!/bin/bash
echo "🔍 Running Babbel override integrity scan..."
BAD_PATTERNS=(
)
FAILED=0
for pattern in "${BAD_PATTERNS[@]}"; do
if grep -RIn --exclude-dir=.venv --exclude-dir=__pycache__ --exclude-dir=dist --exclude-dir=build --exclude-dir=.git "$pattern" .; then
echo "❌ Forbidden pattern detected: $pattern"
FAILED=1
fi
done
if [ $FAILED -eq 1 ]; then
echo "🛑 Override contamination detected. Fix before proceeding."
exit 1
else
echo "✅ Override scan passed. Babbel core remains pure."
fi
