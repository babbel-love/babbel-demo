def classify_emotion(text: str) -> str:
    t = (text or "").lower()
    if any(w in t for w in ["thank you", "thanks", "great", "awesome", "love"]):
        return "joy"
    if any(w in t for w in ["angry", "hate", "furious", "annoyed", "wtf"]):
        return "anger"
    if any(w in t for w in ["sad", "upset", "depressed", "unhappy", "cry"]):
        return "sad"
    if any(w in t for w in ["worried", "scared", "afraid", "nervous", "anxious"]):
        return "fear"
    if any(w in t for w in ["wow", "surprised", "unexpected", "shocked"]):
        return "surprise"
    if any(w in t for w in ["confused", "idk", "not sure"]):
        return "confused"
    return "neutral"
