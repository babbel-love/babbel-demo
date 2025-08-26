#!/bin/bash
set -euo pipefail

echo "📦 Flattening project..."

# Move all contents out of babbel_official to current dir
mv babbel_official/* .

# Remove the empty parent
rmdir babbel_official || true

echo "✅ Now you're in the root of Babbel_Official/"
ls -1
