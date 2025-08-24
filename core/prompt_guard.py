def validate_node_context(messages: list) -> None:
    roles = [m['role'] for m in messages]
    contents = [m['content'].lower() for m in messages]
    banned_phrases = [
        'as an ai language model',
        'you are a helpful assistant',
        'i\'m sorry',
    ]
    for c in contents:
        for phrase in banned_phrases:
            if phrase in c:
                raise RuntimeError(f'LLM-style fallback language detected: {phrase}')
    if 'system' not in roles:
        raise RuntimeError('Missing system prompt.')
    if not any('node' in c or 'protocol' in c for c in contents):
        raise RuntimeError('Missing node or protocol context.')
