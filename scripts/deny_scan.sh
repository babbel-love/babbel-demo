#!/bin/bash
echo "Scanning for banned GPT patterns..."
grep -rniE 'openai|chatgpt|gpt[-]?[34]|openrouter' . \
  --exclude-dir=.git \
  --exclude-dir=.venv \
  --exclude-dir=__pycache__ \
  --exclude=*.pyc || echo "✅ No violations found."
