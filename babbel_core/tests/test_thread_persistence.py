from babbel_core.thread import ConversationThread, SessionStore
from babbel_core.schema_validation import validate_thread_dict

def test_thread_save_load(tmp_path):
    t = ConversationThread("persist", "openrouter/auto", 0.3, 5)
    t.add_message("user", "Persist me")
    t.save(tmp_path)
    saved = list(tmp_path.glob("*.json"))[0]
    loaded = ConversationThread.load(saved)
    assert loaded.thread_name == "persist"
