import os, tempfile, json
from thread import ConversationThread, SessionStore

def test_metadata_persists_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        s = SessionStore(d)
        t = ConversationThread("Untitled", "openrouter/auto", 0.3, 5)
        t.add_message("user","Hello", meta={"emotion":"joy","intent":"greeting","node":"Embodied Agency"})
        t.add_message("assistant","Hi!", meta={"emotion":"joy","intent":"statement","node":"Embodied Agency"})
        s.save_thread(t)
        t2 = s.load_thread(t.thread_id)
        assert t2.messages[0]["meta"]["emotion"] == "joy"
        assert t2.messages[1]["meta"]["node"] == "Embodied Agency"

def test_rename_updates_both_index_and_file():
    with tempfile.TemporaryDirectory() as d:
        s = SessionStore(d)
        t = ConversationThread("Untitled", "openrouter/auto", 0.3, 5)
        t.add_message("user","Plan trip")
        s.save_thread(t)
        s.rename_thread(t.thread_id, "Trip Plan")
        rows = s.list_sessions()
        assert rows[0]["name"] == "Trip Plan"
        # Check file saved with new name
        t2 = s.load_thread(t.thread_id)
        assert t2.thread_name == "Trip Plan"
