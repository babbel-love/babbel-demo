def detect_cultural_shift(text):
    t = text.lower()
    if any(phrase in t for phrase in ["as an american", "in our culture", "where i come from"]):
        return True
    if any(phrase in t for phrase in ["in china", "in japan", "in europe"]):
        return True
    return False
