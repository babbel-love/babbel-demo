def classify_intent(text: str) -> str:
    t = (text or "").strip().lower()
    if not t:
        return "empty"
    if any(t.startswith(x) for x in ["how ", "how do i", "how to"]):
        return "how"
    if any(t.startswith(x) for x in ["what ", "which ", "where ", "who ", "why ", "when "]):
        return "ask"
    if any(w in t for w in ["please", "could you", "can you", "do this", "make ", "create ", "write "]):
        return "command"
    if any(w in t for w in ["hi", "hello", "hey", "good morning", "good evening"]):
        return "greeting"
    if any(w in t for w in ["thanks", "thank you", "cheers"]):
        return "gratitude"
    return "statement"
