import json

def test_babbel_metadata_complete():
    with open("memory_log.json") as f:
        logs = json.load(f)
    assert logs, "No logs found"
    for entry in logs:
        assert "emotion" in entry
        assert "intent" in entry
        assert "final_reply" in entry or "response" in entry
