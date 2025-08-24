import os, tempfile, json
import importlib.util, sys

def _import_mt(tmp_path):
    p = os.path.join(tmp_path, "memory_tracker.py")
    with open("memory_tracker.py","r",encoding="utf-8") as src, open(p,"w",encoding="utf-8") as dst:
        dst.write(src.read().replace('MEMORY_FILE = "memory_log.json"', f'MEMORY_FILE = "{os.path.join(tmp_path,"mem.json")}"'))
    spec = importlib.util.spec_from_file_location("memory_tracker_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["memory_tracker_under_test"] = mod
    spec.loader.exec_module(mod)
    return mod

def test_log_and_recent_emotions():
    with tempfile.TemporaryDirectory() as d:
        mt = _import_mt(d)
        mt.log_interaction("hi","wonder","explore","raw","final","sid1")
        mt.log_interaction("ok","anger","seek","raw","final","sid1")
        emos = mt.get_recent_emotions(2)
        assert emos[-1] == "anger"
