#!/bin/bash
cd "$(dirname "$0")"

echo "🧹 Babbel Cleanup Preview"
echo "--------------------------"

echo -e "\n🔁 Backup & temp files:"
find . -type f \( -name "*.bak" -o -name "*.old" -o -name "*pre_status*" -o -name "*.DS_Store" \)

echo -e "\n🧪 Orphan test files (outside babbel_core/tests/):"
find . -type f -name "test_*.py" ! -path "./babbel_core/tests/*"

echo -e "\n⚠️ core/ wrappers (check if still used):"
[ -d core ] && find core -type f -name "*.py"

echo -e "\n🔄 Chat or UI duplicates:"
find . -type f \( -regex ".*chat.*\.py.*" -or -name "streamlit_babbel_app.py.*" \)

echo -e "\n✅ Preview complete. No files deleted."
echo "   If this looks good, run the cleanup script next."
