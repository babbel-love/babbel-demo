import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
import os, tempfile, subprocess, sys, json
from thread import SessionStore, ConversationThread

def test_export_all_honors_env_overrides_and_writes_csv(tmp_path):
    sessions_dir = tmp_path / "sessions"
    exports_dir = tmp_path / "exports"
    os.makedirs(sessions_dir, exist_ok=True)
    os.makedirs(exports_dir, exist_ok=True)

    s = SessionStore(str(sessions_dir))
    t = ConversationThread("Demo","openrouter/auto",0.1,5)
    t.add_message("user","Plan release", meta={"emotion":"neutral","intent":"task","node":"Embodied Agency","cultural_explanation":"no cultural shift applied"})
    t.add_message("assistant","Here is a concrete plan.", meta={"emotion":"joy","intent":"statement","node":"Embodied Agency","cultural_explanation":"assistant expanded terse request into actionable steps for clarity."})
    s.save_thread(t)

    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    env["SESSIONS_DIR"] = str(sessions_dir)
    env["EXPORTS_DIR"] = str(exports_dir)
    out = subprocess.run([sys.executable, "scripts/export_all.py"], capture_output=True, text=True, env=env)
    assert out.returncode == 0
    out_csv = exports_dir / "all_sessions.csv"
    assert out_csv.exists()
    text = out_csv.read_text(encoding="utf-8")
    assert "cultural_explanation" in text
    assert "Embodied Agency" in text
