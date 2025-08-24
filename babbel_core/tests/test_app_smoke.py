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
