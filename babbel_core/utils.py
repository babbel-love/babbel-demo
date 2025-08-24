# babbel_core/utils.py
def emotion_to_value(label: str) -> float:
    mapping = {
        "shame": -2.0, "grief": -1.5, "anger": -1.0, "fear": -0.5,
        "mixed": 0.0, "curious": 0.25, "wonder": 0.5, "relief": 1.0, "calm": 1.25
    }
    return mapping.get(label, 0.0)
