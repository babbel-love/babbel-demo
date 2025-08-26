#!/bin/bash
echo "🔍 Searching for duplicate review/test files in babbel_core..."

echo "All review.py files:"
find . -type f -name "review.py"

echo ""
echo "All test_review.py files:"
find . -type f -name "test_review.py"

echo ""
echo "Duplicate test filenames:"
find . -type f -name "test_*.py" | xargs -n1 basename | sort | uniq -d

echo ""
echo "Duplicate Python files by content:"
find . -type f -name "*.py" -exec md5sum {} + | sort | uniq -w32 -d
