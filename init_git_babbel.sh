#!/bin/bash
cd "$(pwd)"

echo "🔧 Initializing Git repository..."

git init
git remote add origin git@github.com:babbel-love/babbel-demo.git
git add .
git commit -m "🎉 Initial commit: full working Babbel Core"
git branch -M main
git push -u origin main

echo "✅ Git is now connected to babbel-love/babbel-demo"
