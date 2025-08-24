import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
import os, subprocess, sys

def test_print_tree_outputs_file(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    out = subprocess.check_output([sys.executable, "scripts/print_tree.py"], env=env).decode().strip()
    assert out.endswith(".txt")
    assert os.path.exists(out)
    with open(out, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Project Structure" in content
