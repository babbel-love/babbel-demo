from typing import List, Dict

def validate_message_list(messages: List[Dict]) -> bool:
    return all(isinstance(m, dict) and "role" in m and "content" in m for m in messages)

def validate_roles(messages: List[Dict]) -> bool:
    return all(m["role"] in ["user", "assistant", "system"] for m in messages)
