import tempfile
from thread import ConversationThread, SessionStore

def test_search_sessions_matches_name_and_id():
    with tempfile.TemporaryDirectory() as d:
        s = SessionStore(d)
        a = ConversationThread("Trip to Japan","openrouter/auto",0.2,5); a.add_message("user","plan"); s.save_thread(a)
        b = ConversationThread("Grocery list","openrouter/auto",0.2,5); b.add_message("user","milk"); s.save_thread(b)
        rows = s.search_sessions("japan")
        assert len(rows) == 1 and rows[0]["name"].startswith("Trip")
        rows2 = s.search_sessions(a.thread_id[:4])
        assert len(rows2) >= 1
