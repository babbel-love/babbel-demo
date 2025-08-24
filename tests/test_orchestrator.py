import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")

def test_orchestrate_returns_final_and_meta():
    res = orchestrate("Hi there, can you help?", "Maybe I can help. Let's just try a bit.")
    assert "final_text" in res and "user_meta" in res and "assistant_meta" in res
    assert res["assistant_meta"]["intent"] in {"statement","task","question","greeting","gratitude","farewell"}
    assert "maybe" not in res["final_text"].lower()
    assert res["final_text"].strip()[-1] in ".!?"

    assert set(meta.keys()) == {"emotion","intent","node"}
