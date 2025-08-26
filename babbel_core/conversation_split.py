def split_if_too_long(text: str, max_tokens: int = 300) -> list:
    words = text.split()
    if len(words) <= max_tokens:
        return [text]
    chunks = []
    for i in range(0, len(words), max_tokens):
        chunks.append(" ".join(words[i:i + max_tokens]))
    return chunks
