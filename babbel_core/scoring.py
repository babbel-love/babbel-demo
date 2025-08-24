def score_emotion_confidence(emotion, text):
    return 0.95 if emotion in text.lower() else 0.5

def score_node_match(text, expected_node):
    return 1.0 if expected_node.lower() in text.lower() else 0.0
