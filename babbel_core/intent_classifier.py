def classify_intent(text):
    t = text.lower()
    if any(w in t for w in ["what should", "need advice", "help me"]): return "seek guidance"
    if any(w in t for w in ["i'm sorry", "i am sorry", "my fault", "i feel guilty"]): return "confession"
    if any(w in t for w in ["you always", "why would you", "never listen"]): return "protest"
    if any(w in t for w in ["why", "what does it mean", "what's wrong with me"]): return "search for meaning"
    return "general"
