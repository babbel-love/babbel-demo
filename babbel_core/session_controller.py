from core.session_state import SessionState

class SessionController:
    def __init__(self):
        self.state = SessionState()

    def update_settings(self, protocol: bool, tracker: bool, culture: bool):
        self.state.toggle_protocol(protocol)
        self.state.toggle_tracker(tracker)
        self.state.toggle_culture_shift(culture)

    def get_settings(self):
        return {
            "protocol": self.state.protocol_enabled,
            "tracker": self.state.tracker_enabled,
            "culture": self.state.culture_shift_enabled
        }

    def log_emotion(self, emotion):
        self.state.log_emotion(emotion)
        return self.state.emotion_log
