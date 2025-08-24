def classify_emotion(text):
    t = text.lower()
    if any(w in t for w in ["worthless", "disgust", "ashamed"]): return "shame"
    if any(w in t for w in ["sad", "heartbroken", "loss"]): return "grief"
    if any(w in t for w in ["angry", "rage", "fed up"]): return "anger"
    if any(w in t for w in ["curious", "what if", "open to"]): return "wonder"
    if any(w in t for w in ["scared", "anxious", "afraid"]): return "fear"
    return "mixed"
