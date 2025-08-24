from core.thread import ConversationThread, SessionStore
from core.schema import validate_thread_dict

def test_index_op():
    t = ConversationThread("index", "openrouter/auto", 0.5, 10)
    t.add_message("user", "test")
    assert t.messages[0]["role"] == "user"
