class SessionState:
    def __init__(self):
        self.protocol_enabled = True
        self.tracker_enabled = True
        self.culture_shift_enabled = True
        self.emotion_log = []

    def toggle_protocol(self, state: bool):
        self.protocol_enabled = state

    def toggle_tracker(self, state: bool):
        self.tracker_enabled = state

    def toggle_culture_shift(self, state: bool):
        self.culture_shift_enabled = state

    def log_emotion(self, emotion: str):
        self.emotion_log.append(emotion)
        if len(self.emotion_log) > 100:
            self.emotion_log = self.emotion_log[-100:]
