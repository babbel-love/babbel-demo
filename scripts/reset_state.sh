#!/bin/bash
echo "🧼 Resetting Babbel state files..."
rm -rf .pytest_cache __pycache__ *.log *.tmp *.bak
find . -name "*.pyc" -delete
echo "✅ State reset complete."
