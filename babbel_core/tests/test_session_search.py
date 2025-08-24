from babbel_core.thread import ConversationThread, SessionStore
from babbel_core.schema_validation import validate_thread_dict

def test_searchable_content():
    t = ConversationThread("search", "openrouter/auto", 0.1, 5)
    t.add_message("user", "Search test")
    found = any("Search" in m["content"] for m in t.messages)
    assert found
