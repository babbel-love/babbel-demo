#!/bin/bash
echo "🔐 Installing GitHub CLI and starting login..."

if ! command -v gh &> /dev/null; then
  brew install gh
fi

gh auth login

echo "✅ GitHub CLI authenticated. You can now run: gh run view --web"
