import sys; sys.path.insert(0, "babbel_core")
import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
from core.pipeline import run
def test_pipeline_offline_runs():
    import os
    os.environ["BABBEL_OFFLINE"]="1"
    text,meta=run("Hello there")
    assert isinstance(text,str) and text.strip()
    assert meta["cultural_explanation"]
