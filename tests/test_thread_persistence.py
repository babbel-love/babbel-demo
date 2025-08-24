import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
import os, json, tempfile
from thread import ConversationThread, SessionStore

def test_save_and_load_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        store = SessionStore(d)
        t = ConversationThread("Untitled", "openrouter/auto", 0.3, 5)
        t.add_message("user", "Hello")
        t.add_message("assistant", "Hi—how can I help?")
        path = store.save_thread(t)
        assert os.path.exists(path)
        t2 = store.load_thread(t.thread_id)
        assert t2.thread_id == t.thread_id
        assert t2.messages == t.messages
        # index present
        assert store.list_sessions()[0]["thread_id"] == t.thread_id

def test_auto_title_from_first_user_message():
    with tempfile.TemporaryDirectory() as d:
        store = SessionStore(d)
        t = ConversationThread("Untitled", "openrouter/auto", 0.0, 2)
        t.add_message("user", "Plan my trip to Japan in April")
        store.save_thread(t)
        rows = store.list_sessions()
        assert "Japan" in rows[0]["name"]
