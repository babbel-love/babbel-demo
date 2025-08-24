from core.thread import ConversationThread, SessionStore
from core.schema import validate_thread_dict

def test_metadata_fields():
    t = ConversationThread("meta", "openrouter/auto", 0.2, 5)
    t.add_message("user", "Test")
    assert isinstance(t.to_dict(), dict)
