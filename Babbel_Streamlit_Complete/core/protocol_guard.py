def enforce_protocol_guard(messages):
    for msg in messages:
        if "chatgpt" in msg["content"].lower():
            raise ValueError("GPT-style phrasing detected.")
