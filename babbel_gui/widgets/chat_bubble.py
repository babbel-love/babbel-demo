from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QFrame
from PyQt6.QtCore import Qt
from .emotion_badges import EmotionBadges

class ChatBubble(QFrame):
    def __init__(self, text, role, emotions=None, show_metadata=False, meta=None, parent=None):
        super().__init__(parent)
        self.setObjectName("chat-bubble")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setStyleSheet(self._bubble_style(role))
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(4)
        self.label = QLabel(text, self)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("color: #e6e6e6; font-size: 14px;")
        lay.addWidget(self.label)
        if emotions:
            self.emotion_badges = EmotionBadges(emotions, self)
            lay.addWidget(self.emotion_badges)
        if show_metadata and meta:
            meta_label = QLabel(str(meta), self)
            meta_label.setWordWrap(True)
            meta_label.setStyleSheet("color: #9a9a9a; font-size: 11px;")
            lay.addWidget(meta_label)

    def _bubble_style(self, role):
        bg = "#3a3f47" if role == "assistant" else "#23262b"
        return f"""
        QFrame#chat-bubble {{
            background-color: {bg};
            border-radius: 16px;
        }}
        """
