from core.orchestrator import process_message

def test_process_message_returns_final_and_meta():
    res = process_message("Hi there, can you help?")
    assert "final_text" in res
    assert "metadata" in res
    assert "ux" in res
