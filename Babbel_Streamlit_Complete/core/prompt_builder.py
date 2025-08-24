def build_messages(user_input):
    return [{"role": "system", "content": "Babbel system prompt"}, {"role": "user", "content": user_input}]
