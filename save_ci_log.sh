#!/bin/bash
REPO="babbel-love/babbel-demo"

if ! command -v gh &> /dev/null; then
  echo "❌ GitHub CLI not found. Install from https://cli.github.com/"
  exit 1
fi

gh auth status || exit 1

RUN_ID=$(gh run list -L1 --repo "$REPO" --json databaseId -q '.[0].databaseId')
if [[ -z "$RUN_ID" ]]; then
  echo "❌ No recent CI run found."
  exit 1
fi

gh run view "$RUN_ID" --repo "$REPO" --log > ci_failure_log.txt
echo "✅ Saved: ci_failure_log.txt"
