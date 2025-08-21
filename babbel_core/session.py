from typing import Dict, List

class SessionState:
    def __init__(self):
        self.messages: List[Dict] = []
        self.show_metadata: bool = True
        self.memory: Dict = {}
        self.session_emotions: List[Dict] = []

    def add_message(self, role: str, content: str, meta: Dict = None, emotions: Dict = None):
        msg = {"role": role, "content": content, "meta": meta or {}, "emotions": emotions or {}}
        self.messages.append(msg)
        if emotions:
            self.session_emotions.append(emotions)
