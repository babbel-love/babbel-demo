def explain_cultural_shift(text):
    t = text.lower()
    if "japan" in t:
        return "Note: This may reflect Japanese norms around indirect communication."
    if "america" in t:
        return "Note: This likely stems from American values around individualism."
    if "middle east" in t:
        return "Note: Consider cultural expectations around family and respect."
    return "No cultural shift explanation detected."
