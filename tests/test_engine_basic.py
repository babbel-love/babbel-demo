import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
from engine import BabbelEngine
def test_engine_send_returns_metadata_and_text():
    eng = BabbelEngine()
    out = eng.send("I'm worried about the deadline. Maybe we can plan?")
    assert isinstance(out, dict)
    assert "text" in out and "metadata" in out
    md = out["metadata"]
    assert set(["emotion","intent","node"]).issubset(set(md.keys()))
    assert md["emotion"] in {"fear","joy","sadness","anger","surprise","neutral"}
    assert "maybe" not in out["text"].lower()
