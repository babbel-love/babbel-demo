from babbel.core.protocol_retry import BabbelEngineRetry
class BabbelGUIRetry:
    def __init__(self):
        self.engine = BabbelEngineRetry()
        self.session_history = []
    def send_user_input(self, text: str):
        try:
            response = self.engine.send(text, strict=True)
        except RuntimeError as e:
            response = {"text": str(e), "metadata": {"emotion": None, "node": None}}
        self.session_history.append({"user": text,"assistant": response["text"],"metadata": response["metadata"]})
        return response["text"]
    def get_last_emotion(self):
        if self.session_history:
            return self.session_history[-1]["metadata"]["emotion"]
        return None
    def get_last_node(self):
        if self.session_history:
            return self.session_history[-1]["metadata"]["node"]
        return None
