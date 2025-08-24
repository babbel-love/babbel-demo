import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
import os, subprocess, sys, tempfile, json
from thread import SessionStore, ConversationThread

def run_cli(args, cwd=None, env=None):
    cmd = [sys.executable, "scripts/session_cli.py"] + args
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=env or os.environ.copy())

def test_cli_list_and_duplicate_and_rename(tmp_path):
    sess = tmp_path / "sessions"
    os.makedirs(sess, exist_ok=True)
    s = SessionStore(str(sess))
    t = ConversationThread("Alpha","openrouter/auto",0.3,5)
    t.add_message("user","hello")
    s.save_thread(t)

    r1 = run_cli(["--dir", str(sess), "list"])
    assert r1.returncode == 0
    assert t.thread_id in r1.stdout

    r2 = run_cli(["--dir", str(sess), "duplicate", t.thread_id])
    assert r2.returncode == 0
    dup_id = r2.stdout.strip()
    assert dup_id and dup_id != t.thread_id

    r3 = run_cli(["--dir", str(sess), "rename", dup_id, "Bravo"])
    assert r3.returncode == 0

    r4 = run_cli(["--dir", str(sess), "list"])
    assert "Bravo" in r4.stdout

def test_cli_export_csv(tmp_path):
    sess = tmp_path / "sessions"
    exp = tmp_path / "exports"
    os.makedirs(sess, exist_ok=True)
    s = SessionStore(str(sess))
    t = ConversationThread("Report","openrouter/auto",0.1,5)
    t.add_message("user","hello", meta={"emotion":"joy","intent":"greeting","node":"Embodied Agency","cultural_explanation":"no cultural shift applied"})
    s.save_thread(t)

    r = run_cli(["--dir", str(sess), "export-csv", t.thread_id, "--out", str(exp), "--name", "x.csv"])
    assert r.returncode == 0
    outp = r.stdout.strip()
    assert outp.endswith("x.csv") and os.path.exists(outp)
