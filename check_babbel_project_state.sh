#!/bin/bash
cd "$(dirname "$0")"
echo "📂 Babbel Project: Clean State Report"
echo "--------------------------------------"

echo -e "\n🧱 Repo root files:"
find . -maxdepth 1 -type f ! -name ".*" ! -name "*.sh" ! -name "*.md" ! -name "*.json" -exec basename {} \;

echo -e "\n📁 babbel_core contents (top level):"
find babbel_core -maxdepth 1 -type f -exec basename {} \;

echo -e "\n📁 babbel_core folders:"
find babbel_core -mindepth 1 -type d ! -name "__pycache__"

echo -e "\n🧪 Tests remaining:"
find babbel_core/tests -type f -name "test_*.py" 2>/dev/null || echo "(none)"

echo -e "\n🚫 Ignored: .venv/ and .trash_cleanup/"
