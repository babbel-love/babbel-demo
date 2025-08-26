def carry_context_if_needed(text: str) -> str:
    if len(text.split()) > 100:
        return "Earlier context suggests: " + text
    return text
