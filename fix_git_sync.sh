#!/bin/bash

cd ~/Babbel_Official || exit 1

# Ensure .git exists and create branch if HEAD is missing
git rev-parse --is-inside-work-tree 2>/dev/null || git init
git symbolic-ref --quiet HEAD >/dev/null || git checkout -B main

BRANCH_NAME="$(git symbolic-ref --short HEAD 2>/dev/null || echo main)"
echo "Using branch: $BRANCH_NAME"

# Add remote if not present
REMOTE_URL="git@github.com:YOUR/REPO.git"
if ! git remote | grep -q '^origin$'; then
  git remote add origin "$REMOTE_URL"
fi

# Add a standard .gitignore
cat > .gitignore <<'EOF'
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/
dist/
build/
.venv/
.venv*/
.env
.env.*
.DS_Store
memory_log.json
EOF

# Stage, commit, and push
git add -A
git status -s
git commit -m "Initial sync of Babbel Core project" || echo "Nothing to commit"
git push -u origin "$BRANCH_NAME"

git status
