from babbel_core.engine import BabbelEngine

def test_engine_responds():
    engine = BabbelEngine()
    out = engine.send("Hello?")
    assert isinstance(out, dict)
    assert "text" in out or "final_text" in out
