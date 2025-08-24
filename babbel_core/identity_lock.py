def validate_identity(message: str) -> bool:
    return not any(x in message.lower() for x in ["chatgpt", "openai", "gpt-4"])

def enforce_identity_lock(messages: list):
    for msg in messages:
        if not validate_identity(msg["content"]):
            raise PermissionError("Identity lock triggered by prohibited reference.")
