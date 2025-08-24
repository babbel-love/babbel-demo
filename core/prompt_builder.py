def build_messages(user_input: str):
    return [
        {"role": "system", "content": "You are Babbel, a local deterministic assistant."},
        {"role": "user", "content": user_input}
    ]
