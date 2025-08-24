from core.pipeline import run_pipeline

def test_pipeline_formatting_contains_required_sections():
    result = run_pipeline("How do I back up my photos?")
    assert "final_text" in result
    assert "choices" in result["ux"]
    assert "emotion" in result["metadata"]
