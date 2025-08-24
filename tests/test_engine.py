import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
from core.engine import BabbelEngine
def test_engine_roundtrip_and_csv(tmp_path,monkeypatch):
    monkeypatch.setenv("BABBEL_OFFLINE","1")
    e=BabbelEngine()
    out=e.reply("Test session start")
    assert out["metadata"]["tone"]=="direct"
    csvp=e.export_csv()
    assert csvp.endswith(".csv")
