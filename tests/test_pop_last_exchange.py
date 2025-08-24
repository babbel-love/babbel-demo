import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
from thread import ConversationThread

def test_pop_last_exchange_removes_pair():
    t = ConversationThread("T","openrouter/auto",0.1,5)
    t.add_message("user","u1")
    t.add_message("assistant","a1")
    t.add_message("user","u2")
    t.add_message("assistant","a2")
    t.pop_last_exchange()
    assert [m["content"] for m in t.messages] == ["u1","a1"]
    # popping again removes first pair
    t.pop_last_exchange()
    assert t.messages == []
    # popping on empty is safe
    t.pop_last_exchange()
    assert t.messages == []
