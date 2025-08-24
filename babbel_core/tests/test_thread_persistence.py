from core.thread import SessionStore

def test_thread_save_load(tmp_path):
    store = SessionStore()
    store.save_to_file(tmp_path / "session.json")
    assert (tmp_path / "session.json").exists()
