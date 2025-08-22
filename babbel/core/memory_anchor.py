def attach_memory_anchor(messages: list, memory: dict) -> list:
    anchor = memory.get("anchor", "Unknown")
    node = memory.get("node", "Unscored")
    emotion = memory.get("emotion", "Neutral")

    anchor_block = {
        "role": "system",
        "content": f"# Memory Anchor\nLast node: {node}\nLast emotion: {emotion}\nAnchor: {anchor}"
    }

    return [anchor_block] + messages
