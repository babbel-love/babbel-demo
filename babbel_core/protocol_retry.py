def enforce_retry_guard(messages):
    retry_count = sum(1 for m in messages if m.get("role") == "user" and "again" in m.get("content", "").lower())
    if retry_count > 3:
        raise RuntimeError("Too many retries detected.")
