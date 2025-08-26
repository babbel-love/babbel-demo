from ..intent_classifier import classify_intent

def test_confession_detect():
    assert classify_intent("I’m sorry, it’s my fault") == "confession"

def test_protest_detect():
    assert classify_intent("You always do this to me") == "protest"
