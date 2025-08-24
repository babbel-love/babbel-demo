from babbel_core.thread import SessionStore, ConversationThread
from babbel_core.schema_validation import validate_thread_dict

def test_export_saving(tmp_path):
    thread = ConversationThread("test", "openrouter/auto", 0.5, 10)
    thread.add_message("user", "Hi")
    thread.add_message("assistant", "Hello.")
    thread.save(tmp_path)
    path = list(tmp_path.glob("*.json"))[0]
    data = validate_thread_dict(path)
    assert data["thread_name"] == "test"
