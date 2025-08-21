def apply_protocol_rules(text: str, tone: str, emotion: str, intent: str) -> tuple[str, str]:
    notes = []
    rewritten = text
    if tone == 'dismissive':
        notes.append("Tone was dismissive; softened language.")
        rewritten = rewritten.replace('whatever', 'I see').replace('just', '')
    if emotion == 'angry':
        notes.append("Detected anger; encouraged calming phrasing.")
        rewritten = rewritten.replace('furious', 'concerned')
    if intent == 'question' and not text.strip().endswith('?'):
        notes.append("Added question mark for clarity.")
        rewritten += '?'
    return rewritten.strip(), ' '.join(notes)
