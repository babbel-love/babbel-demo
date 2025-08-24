#!/bin/bash
set -e

echo "📦 Moving all core files into babbel_core/ package..."

mkdir -p babbel_core
mv *.py babbel_core/ 2>/dev/null || true
touch babbel_core/__init__.py

echo "🧪 Updating PYTHONPATH in tests..."
find tests/ -name "test_*.py" -exec sed -i '' '1i\
import sys; sys.path.insert(0, "babbel_core")
' {} +

echo "✅ Committing new structure..."
git add babbel_core/ tests/
git commit -m "📦 Restructure as babbel_core package to fix import errors"
git push
