from babbel.core.hx_engine import build_extras

def test_build_and_compose():
    out = build_extras("This is a message.", "neutral", "curious", "neutral")
    assert "ux" in out
    assert "reflection" in out["ux"]
