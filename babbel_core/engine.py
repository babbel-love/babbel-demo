from core.prompt_builder import build_messages
from core.protocol_guard import enforce_protocol_guard
from core.memory_tracker import attach_memory_anchor
from core.pipeline import run_pipeline

class BabbelEngine:
    def __init__(self):
        self.memory = {
            "anchor": "start",
            "node": "None",
            "emotion": "Neutral"
        }

    def _safe_call_to_model(self, messages):
        return run_pipeline(messages[-1]["content"])

    def send(self, user_input: str, strict: bool = True) -> dict:
        msgs = build_messages(user_input)
        msgs = attach_memory_anchor(msgs, self.memory)
        if strict:
            enforce_protocol_guard(msgs)
        response = self._safe_call_to_model(msgs)
        self.memory["anchor"] = "latest"
        self.memory["node"] = response["metadata"]["node"]
        self.memory["emotion"] = response["metadata"]["emotion"]
        return {
            "final_text": response["final_text"],
            "metadata": response["metadata"],
            "ux": response["ux"]
        }
