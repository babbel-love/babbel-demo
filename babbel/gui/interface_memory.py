from babbel.core.engine_memory import BabbelEngineMemory

class BabbelGUIInterface:
    def __init__(self):
        self.engine = BabbelEngineMemory()
        self.session_history = []

    def send_user_input(self, text: str):
        response = self.engine.send(text, strict=True)
        self.session_history.append({
            "user": text,
            "assistant": response["text"],
            "metadata": response["metadata"]
        })
        return response["text"]

    def get_last_emotion(self):
        if self.session_history:
            return self.session_history[-1]["metadata"]["emotion"]
        return None

    def get_last_node(self):
        if self.session_history:
            return self.session_history[-1]["metadata"]["node"]
        return None
