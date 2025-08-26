#!/bin/bash
cd "$(dirname "$0")"
echo "🔍 FINAL SANITY SCAN — Babbel Project"

echo -e "\n🔹 Orphan .py files (no imports found):"
find babbel_core -maxdepth 1 -type f -name "*.py" | while read file; do
  fname=$(basename "$file" .py)
  used=$(grep -r "$fname" babbel_core --exclude="$file" --exclude-dir=".trash_cleanup" --exclude-dir="__pycache__" | wc -l)
  [ "$used" -eq 0 ] && echo "❌ Possibly orphaned: $file"
done

echo -e "\n🧹 __pycache__ folders:"
find . -type d -name "__pycache__"

echo -e "\n📦 .egg-info folders:"
find . -type d -name "*.egg-info"

echo -e "\n🧪 test files still present:"
find babbel_core/tests -type f -name "test_*.py" 2>/dev/null || echo "(none)"

echo -e "\n📁 Anything still in .trash_cleanup:"
find .trash_cleanup -type f | wc -l | xargs echo "🗑️  Files in .trash_cleanup:"

echo -e "\n✅ Final scan complete. Almost there."
