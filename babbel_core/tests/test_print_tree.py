from babbel_core import thread

def test_thread_serialization():
    t = thread.ConversationThread("Test", "openrouter/auto", 0.5, 5)
    t.add_message("user", "Hi")
    t.add_message("assistant", "Hello")
    d = t.to_dict()
    assert isinstance(d, dict)
    assert "messages" in d
    assert any(m["role"] == "user" for m in d["messages"])
    assert any(m["role"] == "assistant" for m in d["messages"])
