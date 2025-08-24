from core.review import run_review_stage

def test_review_stage_basic():
    result = run_review_stage("This is just a test. Maybe helpful.")
    assert isinstance(result, dict)
    assert "reviewed_text" in result
