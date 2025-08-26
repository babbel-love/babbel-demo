#!/bin/bash
set -e
echo "🔄 Syncing Babbel project with GitHub..."
git add .
git commit -m "🔄 Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
