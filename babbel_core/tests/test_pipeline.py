from ..pipeline import run_pipeline

def test_pipeline_response():
    out = run_pipeline("I feel ashamed and want to disappear.")
    assert "you’re holding something unbearable" in out.lower()
    assert "babbel voice" in out.lower()
    assert "fact" in out.lower()
