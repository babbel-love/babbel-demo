def classify_tone(text: str) -> str:
    lowered = text.lower()
    if '?' in text: return 'inquisitive'
    if any(word in lowered for word in ['just', 'only', 'whatever']): return 'dismissive'
    if any(word in lowered for word in ['sorry', 'apologize']): return 'apologetic'
    return 'neutral'
