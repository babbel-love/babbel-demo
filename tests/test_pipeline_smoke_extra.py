import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
from pipeline import run_pipeline
def test_pipeline_formatting_contains_required_sections():
    out = run_pipeline("How to back up my photos?")
    assert "Final Answer:" in out
    assert "Quick check:" in out
