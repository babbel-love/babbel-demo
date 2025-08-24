from core import prompt_builder, protocol_guard, memory_anchor

class BabbelEngine:
    def __init__(self):
        self.memory = {"anchor": "start", "node": "None", "emotion": "Neutral"}

    def _safe_call_to_model(self, messages):
        return {
            "text": "Processed with anchored memory and retry check.",
            "metadata": {
                "emotion": self.memory.get("emotion"),
                "tone": "detached",
                "node": self.memory.get("node")
            }
        }

    def send(self, user_input: str, strict: bool = True) -> dict:
        msgs = prompt_builder.build_messages(user_input)
        msgs = memory_anchor.attach_memory_anchor(msgs, self.memory)
        if strict:
            protocol_guard.enforce_protocol_guard(msgs)
        response = self._safe_call_to_model(msgs)
        self.memory["anchor"] = "latest"
        self.memory["node"] = response["metadata"]["node"]
        self.memory["emotion"] = response["metadata"]["emotion"]
        return response
