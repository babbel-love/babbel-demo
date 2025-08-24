#!/bin/bash
set -e
echo "📥 Pulling latest from GitHub..."
git fetch origin
git reset --hard origin/main
git clean -fd
echo "✅ Babbel project is now fully updated to latest main branch."
