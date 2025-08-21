from babbel.core.orchestrator import process_message

def test_fallback_path_runs():
    payload = {"text": "Give me one tiny next step to start writing again."}
    out = process_message(payload)
    assert "final_text" in out
    assert "ux" in out
