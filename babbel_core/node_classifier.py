def classify_node(text):
    t = text.lower()
    if "i give up" in t or "it's pointless" in t:
        return "Collapsed Despair"
    if "i want to try" in t or "i can do this" in t:
        return "Embodied Agency"
    if "i don't know" in t or "i feel stuck" in t:
        return "Reflective Uncertainty"
    if "you always" in t or "this isn't fair" in t:
        return "Protest"
    return "Unclassified"
