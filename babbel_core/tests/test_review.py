from ..review import run_review_stage

def test_review_response():
    result = run_review_stage("This might help, perhaps.")
    assert isinstance(result, dict)
    assert "reviewed_text" in result
    assert "babbel" in result["quick_check"].lower()
