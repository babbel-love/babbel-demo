from babbel.core.culture_shift import apply_and_explain

def test_soften():
    text = "You should always try harder."
    result, explanation = apply_and_explain(text)
    assert "could" in result or "often" in result
    assert explanation == "softened directive tone"

def test_unknown():
    text = "Hello there."
    result, explanation = apply_and_explain(text)
    assert result == text
    assert "left unchanged" in explanation
