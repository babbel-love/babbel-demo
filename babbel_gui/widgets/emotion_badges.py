from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

class EmotionBadges(QWidget):
    def __init__(self, emotions, parent=None):
        super().__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        for emo, score in (emotions or {}).items():
            lbl = QLabel(f"{emo} {score:.2f}")
            lbl.setStyleSheet("font-size: 10px; color: #aaa; padding: 2px;")
            lay.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignLeft)
