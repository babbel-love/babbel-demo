from babbel.core import protocol_guard, memory_anchor, prompt_builder

class BabbelEngineRetry:
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

    def send(self, user_input: str, strict: bool = True, max_retries: int = 3) -> dict:
        attempt = 0
        while attempt < max_retries:
            msgs = prompt_builder.build_messages(user_input)
            msgs = memory_anchor.attach_memory_anchor(msgs, self.memory)
            if strict:
                try:
                    protocol_guard.enforce_protocol_guard(msgs)
                except RuntimeError:
                    attempt += 1
                    continue
            response = self._safe_call_to_model(msgs)
            self.memory["anchor"] = "latest"
            self.memory["node"] = response["metadata"]["node"]
            self.memory["emotion"] = response["metadata"]["emotion"]
            return response
        raise RuntimeError("Protocol retry failed: maximum attempts reached")
