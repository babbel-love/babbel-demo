from ..emotion_classifier import classify_emotion

def test_detect_shame():
    assert classify_emotion("I feel ashamed and disgusting") == "shame"

def test_detect_wonder():
    assert classify_emotion("What if I did something meaningful?") == "wonder"
