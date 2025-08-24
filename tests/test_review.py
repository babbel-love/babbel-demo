import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
from review import enforce_tone_and_style, summarize_flags

def test_enforce_tone_and_style_removes_hedges_and_closes_sentence():
    out = enforce_tone_and_style("This is just a bit messy, maybe fix it")
    assert "maybe" not in out.lower()
    assert out.strip()[-1] in ".!?"

def test_summarize_flags_counts_hedges():
    info = summarize_flags("I think we could maybe just try a bit?")
    assert info["count"] >= 3
    assert "maybe" in info["hedges_found"]
