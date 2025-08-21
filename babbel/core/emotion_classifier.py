def classify_emotion(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in ['sad', 'disappointed', 'upset']): return 'sad'
    if any(word in lowered for word in ['angry', 'mad', 'furious']): return 'angry'
    if any(word in lowered for word in ['anxious', 'worried', 'nervous']): return 'anxious'
    if any(word in lowered for word in ['happy', 'excited', 'grateful']): return 'happy'
    return 'neutral'
