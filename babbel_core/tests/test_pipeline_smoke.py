from core.pipeline import run_pipeline

def test_pipeline_runs():
    result = run_pipeline("How do I back up my photos?")
    assert isinstance(result, dict)
    assert "final_text" in result
    assert "metadata" in result
    assert "ux" in result
