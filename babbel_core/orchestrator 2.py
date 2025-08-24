from node_classifier import classify_node
from tone_classifier import classify_tone
from intent_classifier import classify_intent
from emotion_classifier import classify_emotion

def orchestrate_response(text):
    node = classify_node(text)
    tone = classify_tone(text)
    intent = classify_intent(text)
    emotion = classify_emotion(text)
    return {
        "node": node,
        "tone": tone,
        "intent": intent,
        "emotion": emotion
    }
