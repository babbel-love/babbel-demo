from core.schema import validate_payload

def test_validate_and_roundtrip():
    obj = {
        "messages": [{"role": "user", "content": "Hi"}],
        "metadata": {"node": "None", "emotion": "Neutral", "intent": "greeting"}
    }
    fp = validate_payload(obj)
    assert isinstance(fp, dict)
