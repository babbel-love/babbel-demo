def classify_intent(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in ['how', 'what', 'why', 'can you']): return 'question'
    if any(word in lowered for word in ['thanks', 'appreciate']): return 'gratitude'
    if any(word in lowered for word in ['i think', 'i believe']): return 'opinion'
    return 'statement'
