#!/bin/bash
cd "$(dirname "$0")"
echo "📦 Deep Audit: Babbel_Official Project"
echo "----------------------------------------"

echo -e "\n🔁 Backup-style filenames:"
find . -type f \( -name "*.bak" -o -name "*.old" -o -name "*backup*" -o -name "*pre_status*" \)

echo -e "\n💀 Possibly empty or tiny .py files:"
find . -type f -name "*.py" -size -1k

echo -e "\n⚠️ Legacy or unused scripts:"
find . -type f -name "*.py" | grep -Ei '(backup|probe|run|old|v1|v2|copy|refactor)'

echo -e "\n🧪 Test files outside /tests/:"
find . -type f -name "test_*.py" ! -path "*/tests/*"

echo -e "\n🐍 Virtualenv clutter:"
find . -type f \( -name "pyvenv.cfg" -o -name "Pipfile.lock" -o -name "poetry.lock" -o -name "*.egg-info" \)

echo -e "\n📁 Hidden metadata folders:"
find . -type d -name ".*" ! -name ".git" ! -name ".venv"

echo -e "\n🗃️  Other large or strange files (>1MB or odd ext):"
find . -type f -size +1M -exec ls -lh {} \;
find . -type f -regex ".*\.\(log\|csv\|sqlite\|jsonl\|dump\|db\)"

echo -e "\n✅ Audit complete. No files were deleted."
