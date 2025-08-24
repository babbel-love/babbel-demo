from babbel_core.core.pipeline import run_pipeline

def test_pipeline_response():
    result = run_pipeline("How do I start a fire?")
    assert isinstance(result, dict)
    assert "final_text" in result
