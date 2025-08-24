def classify_tone(text):
    t = text.lower()
    if any(word in t for word in ["please", "thank you", "great", "good job"]): return "friendly"
    if any(word in t for word in ["as per", "therefore", "in conclusion"]): return "formal"
    if any(word in t for word in ["hey", "yo", "lol"]): return "casual"
    if any(word in t for word in ["urgent", "immediately", "critical"]): return "professional"
    return "neutral"
