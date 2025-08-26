def is_generic_response(text):
    banned_phrases = [
        "as an AI language model",
        "I cannot provide",
        "I'm just a program",
    ]
    return any(p in text.lower() for p in banned_phrases)
