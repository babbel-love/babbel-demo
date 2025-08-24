import subprocess, sys

def test_app_smoke_script_runs():
    out = subprocess.run([sys.executable, "scripts/app_smoke.py"], capture_output=True, text=True)
    assert out.returncode == 0
    assert "FINAL:" in out.stdout
    assert "PIPELINE" in out.stdout
