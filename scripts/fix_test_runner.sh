#!/bin/bash
set -e

echo "🔧 Patching test_pipeline_run.py..."
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

echo "🔧 Updating test_app_smoke.py..."
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

echo "✅ Done. Rerunning tests..."
pytest babbel_core/tests --tb=short -q
