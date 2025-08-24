from core.thread import SessionStore, ConversationThread
from core.schema import validate_thread_dict

def test_thread_addition():
    t = ConversationThread("cli", "openrouter/auto", 0.0, 10)
    t.add_message("user", "Test CLI")
    assert t.messages[-1]["content"] == "Test CLI"
