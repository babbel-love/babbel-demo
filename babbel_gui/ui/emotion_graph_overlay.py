from PyQt6.QtWidgets import QLabel

self.emotion_trend_strip = QLabel("")
main_layout.insertWidget(0, self.emotion_trend_strip)

def update_emotion_trend(self, session_emotions):
    if not self.sidebar.tracker_toggle.isChecked():
        self.emotion_trend_strip.setText("")
        return

def update_emotion_trend(self, session_emotions):
    if not self.sidebar.tracker_toggle.isChecked():
        self.emotion_trend_strip.setText("")
        return

# --- Session Emotion Trend Bar ---
from PyQt6.QtWidgets import QLabel

# Call this in your UI init/setup:
# self.emotion_trend_strip = QLabel("")
# main_layout.insertWidget(0, self.emotion_trend_strip)

def update_emotion_trend(self, session_emotions):
    if not self.sidebar.tracker_toggle.isChecked():
        self.emotion_trend_strip.setText("")
        return
    if not session_emotions:
        self.emotion_trend_strip.setText("")
        return
    recent = session_emotions[-16:]
    trend = " | ".join(recent)
    self.emotion_trend_strip.setText(f"Recent emotions: {trend}")
