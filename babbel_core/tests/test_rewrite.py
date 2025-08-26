from ..rewrite import rewrite_tone, enforce_babbel_style

def test_rewrite_tone_removes_hedges():
    text = "I just think maybe we could try."
    out = rewrite_tone(text)
    assert "just" not in out.lower()
    assert "maybe" not in out.lower()

def test_babbel_style_strengthens_phrases():
    text = "It is important to note that we should utilize time."
    out = enforce_babbel_style(text)
    assert "important to note" not in out.lower()
    assert "utilize" not in out.lower()
    assert "should" not in out.lower()
