def send(self, user_input: str, strict: bool = True) -> dict:
    messages = prompt_builder.build_messages(user_input)
    system_texts = [m['content'] for m in messages if m['role'] == 'system']
    full_prompt = '
'.join(system_texts).lower()
    banned_phrases = [
        'you are a helpful assistant',
        'as an ai language model',
        'i'\''m sorry',
    ]
    if strict:
        for phrase in banned_phrases:
            if phrase in full_prompt:
                raise RuntimeError(f'BLOCKED: prompt contains banned phrase → {phrase}')
    return self._safe_call_to_model(messages)

