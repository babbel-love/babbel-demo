def attach_memory_anchor(messages, memory):
    anchor_note = f"(Memory anchor: {memory.get('anchor', 'none')})"
    messages.append({"role": "system", "content": anchor_note})
    return messages
