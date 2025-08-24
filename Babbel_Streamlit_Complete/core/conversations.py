def format_conversation(messages):
    return "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in messages if isinstance(m, dict) and "role" in m and "content" in m)
