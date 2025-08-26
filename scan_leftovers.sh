#!/bin/bash
cd "$(dirname "$0")"

echo "🔍 FINAL LEFTOVERS SCAN"
echo "------------------------"

echo -e "\n📁 Empty folders (excluding .venv):"
find . -type d -empty ! -path "*/.venv/*"

echo -e "\n📦 .egg-info or metadata folders:"
find . -type d -name "*.egg-info"

echo -e "\n💥 .DS_Store and .trash.*:"
find . -type f \( -name ".DS_Store" -o -path "*/.trash.*/*" \)

echo -e "\n📄 Redundant config/log/tmp files:"
find . -type f \( -name "*.log" -o -name "*.gz" -o -name "*.jsonl" -o -name "*.txt" -o -name "*.pid" \) ! -path "*.venv/*"

echo -e "\n🔀 Possibly redundant or overlapping files:"
ls babbel_core/node_*.py 2>/dev/null || echo "(none)"
ls babbel_core/session_*.py 2>/dev/null || echo "(none)"
ls babbel_core/protocol_*.py 2>/dev/null || echo "(none)"

echo -e "\n🧪 Check: test folders still present?"
[ -d babbel_core/tests ] && echo "✅ tests/ found" || echo "❌ No test folder"

echo -e "\n🧼 Suggestion: remove if unused → _quarantine_manual/, .trash.*, adapters/, scripts/"

echo -e "\n✅ Leftover scan complete."
