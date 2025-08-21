from babbel.core.orchestrator import process_message

def test_ux_block_present():
    payload = {"text": "I'm a bit anxious. What should I do?"}
    out = process_message(payload)
    assert "ux" in out
    assert "final_text" in out
