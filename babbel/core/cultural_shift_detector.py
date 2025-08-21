def detect_cultural_shift(text: str) -> str:
    if 'america' in text.lower() or 'europe' in text.lower():
        return "Detected potential regional framing. Adjusted for cultural neutrality."
    if 'holiday' in text.lower():
        return "Note: 'holiday' can vary culturally (vacation vs religious)."
    return "No significant cultural shift detected."
