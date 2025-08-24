#!/bin/bash
set -e

echo "🔧 Step 1: Fix .gitignore..."
cat <<'EOF' > .gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/
dist/
build/

# Virtualenv / env files
.venv/
.env
.env.*

# System
.DS_Store
Thumbs.db

# Babbel session memory
memory_log.json
sessions/
EOF

echo "🔧 Step 2: Patch test_pipeline_run.py with absolute import..."
cat <<'PY' > babbel_core/core/test_pipeline_run.py
from babbel_core.core.pipeline import run_pipeline

def main():
    print("Babbel Pipeline Runner (no GUI)")
    print("-" * 40)
    while True:
        user_input = input("Prompt> ").strip()
        if not user_input or user_input.lower() in ('exit', 'quit'):
            break
        print("\nRunning pipeline...\n")
        response = run_pipeline(user_input)
        print("\n--- FINAL OUTPUT ---")
        print(response)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()
PY

echo "🔧 Step 3: Fix test_app_smoke.py to run module correctly..."
cat <<'PY' > babbel_core/tests/test_app_smoke.py
import subprocess
import sys
import os

def test_app_smoke_script_runs():
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(".")
    out = subprocess.run(
        [sys.executable, "-m", "babbel_core.core.test_pipeline_run"],
        input=b"exit\n", capture_output=True, timeout=5,
        env=env
    )
    assert out.returncode == 0
    assert b"Babbel Pipeline Runner" in out.stdout
PY

echo "🔧 Step 4: Fix test_print_tree.py..."
cat <<'PY' > babbel_core/tests/test_print_tree.py
from babbel_core import thread

def test_thread_serialization():
    t = thread.ConversationThread("Test", "openrouter/auto", 0.5, 5)
    t.add_message("user", "Hi")
    t.add_message("assistant", "Hello")
    d = t.to_dict()
    assert isinstance(d, dict)
    assert "messages" in d
    assert any(m["role"] == "user" for m in d["messages"])
    assert any(m["role"] == "assistant" for m in d["messages"])
PY

echo "🔍 Step 5: Git status check..."
git status -s

echo "✅ Step 6: Run all tests..."
pytest babbel_core/tests --tb=short -q
