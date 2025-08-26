from babbel_core.utils import enforce_babbel_style

def test_enforce_babbel_style_removes_hedges():
    input_text = "I think we should maybe try to sort of use it."
    result = enforce_babbel_style(input_text)
    assert "maybe" not in result
    assert "sort of" not in result
    assert "should" not in result.lower()
    assert "must" in result.lower()
