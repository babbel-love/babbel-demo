from babbel_core.thread import ConversationThread
from babbel_core.schema_validation import validate_thread_dict

def test_last_exchange_removal():
    t = ConversationThread("test", "openrouter/auto", 0.5, 10)
    t.add_message("user", "A")
    t.add_message("assistant", "B")
    assert len(t.messages) == 2
    t.messages.pop()
    assert len(t.messages) == 1
