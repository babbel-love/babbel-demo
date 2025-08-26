#!/bin/bash
echo "🔍 Fetching latest CI run logs..."

REPO="babbel-love/babbel-demo"

if ! command -v gh &> /dev/null; then
  echo "❌ GitHub CLI (gh) not found. Please install it: https://cli.github.com/"
  exit 1
fi

gh auth status || exit 1

RUN_ID=$(gh run list -L1 --repo "$REPO" --json databaseId -q '.[0].databaseId')
if [[ -z "$RUN_ID" ]]; then
  echo "❌ No recent CI run found."
  exit 1
fi

gh run view "$RUN_ID" --repo "$REPO" --log
