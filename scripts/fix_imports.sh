#!/bin/bash
set -e

echo "📦 Creating __init__.py to mark project root as importable module..."

touch __init__.py

echo "✅ __init__.py created. Testing import resolution..."

PYTHONPATH=. pytest tests/ --tb=short -q

echo "✅ Local tests passed. Committing..."

git add __init__.py
git commit -m "🧩 Fix import path for schema_validation module"
git push
