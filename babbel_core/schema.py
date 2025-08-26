from __future__ import annotations

def validate_payload(payload: dict) -> bool:
    if not isinstance(payload, dict): return False
    if "messages" not in payload or not isinstance(payload["messages"], list): return False
    if not any(m.get("role")=="user" for m in payload["messages"] if isinstance(m, dict)): return False
    # Optional: model/temperature if present
    if "model" in payload and not isinstance(payload["model"], str): return False
    if "temperature" in payload:
        try:
            float(payload["temperature"])
        except Exception:
            return False
    return True
