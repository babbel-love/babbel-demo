from babbel_core.engine import BabbelEngine

def test_engine_send_returns_metadata_and_text():
    eng = BabbelEngine()
    out = eng.send("I'm worried about the deadline. Maybe we can plan?")
    assert "final_text" in out
    assert "metadata" in out
    assert "maybe" not in out["final_text"].lower()
