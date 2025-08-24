import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
import os, time, tempfile
from thread import ConversationThread, SessionStore

def test_list_order_by_mtime_desc():
    with tempfile.TemporaryDirectory() as d:
        s = SessionStore(d)
        a = ConversationThread("A","openrouter/auto",0.3,5); a.add_message("user","one"); s.save_thread(a)
        time.sleep(0.02)
        b = ConversationThread("B","openrouter/auto",0.3,5); b.add_message("user","two"); s.save_thread(b)
        rows = s.list_sessions()
        assert rows[0]["thread_id"] == b.thread_id
        assert rows[1]["thread_id"] == a.thread_id

def test_delete_and_rename_affect_index():
    with tempfile.TemporaryDirectory() as d:
        s = SessionStore(d)
        t = ConversationThread("X","openrouter/auto",0.3,5); t.add_message("user","hello"); s.save_thread(t)
        s.rename_thread(t.thread_id, "Renamed")
        rows = s.list_sessions()
        assert rows[0]["name"] == "Renamed"
        s.delete_thread(t.thread_id)
        rows2 = s.list_sessions()
        assert all(r["thread_id"] != t.thread_id for r in rows2)
