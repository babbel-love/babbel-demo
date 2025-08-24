from protocol_guard import enforce_protocol_guard
from protocol_retry import enforce_retry_guard
from identity_lock import enforce_identity_lock

def apply_protocol_stack(messages: list) -> list:
    enforce_identity_lock(messages)
    enforce_protocol_guard(messages)
    enforce_retry_guard(messages)
    return messages
