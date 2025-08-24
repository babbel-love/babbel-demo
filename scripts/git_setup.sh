#!/bin/bash
set -e
echo "🔧 Setting up Git remote and branch for Babbel..."

git init
git remote add origin git@github.com:babbel-love/babbel-demo.git
git branch -M main
git add .
git commit -m "🎉 Initial commit: Babbel setup"
git push -u origin main

echo "✅ Git setup complete and pushed to GitHub."
