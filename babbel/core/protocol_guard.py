def enforce_protocol_guard(messages: list) -> None:
    banned = [
        "as an ai language model",
        "you are a helpful assistant",
        "let me know if you need anything else",
    ]
    for msg in messages:
        content = msg.get("content", "").lower()
        if any(bad in content for bad in banned):
            raise RuntimeError(f"🚨 Protocol violation: {content}")
