from typing import Dict, Any

def validate_final_output(data: Dict[str, Any]) -> Dict[str, Any]:
    required_fields = ["final_text", "metadata", "ux"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing field in output: '{field}'")
    return data

def validate_thread_dict(thread: Dict[str, Any]) -> Dict[str, Any]:
    if "messages" not in thread or not isinstance(thread["messages"], list):
        raise ValueError("Thread must have a 'messages' list")
    if not all("role" in m and "content" in m for m in thread["messages"]):
        raise ValueError("Each message must have 'role' and 'content'")
    return thread

def validate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    if "messages" not in payload:
        raise ValueError("Missing 'messages' in payload")
    return payload

def to_dict(obj: Any) -> Dict[str, Any]:
    return obj.dict() if hasattr(obj, "dict") else dict(obj)
