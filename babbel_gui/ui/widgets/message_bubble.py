from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QApplication
from PyQt6.QtCore import Qt, QDateTime

class MessageBubble(QWidget):
    def __init__(self, text: str, role: str = "assistant", ts: float | None = None, parent=None):
        super().__init__(parent)
        wrap = QVBoxLayout(self); wrap.setContentsMargins(0,0,0,0); wrap.setSpacing(4)
        frame = QFrame(self)
        frame.setObjectName("bubble")
        frame.setStyleSheet("#bubble{background:#222;border-radius:16px;padding:10px;color:#eaeaea}")
        inner = QVBoxLayout(frame); inner.setContentsMargins(12,8,12,8); inner.setSpacing(8)
        self.body = QLabel(text); self.body.setWordWrap(True)
        self.body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        inner.addWidget(self.body)
        row = QHBoxLayout(); row.setContentsMargins(0,0,0,0); row.setSpacing(8)
        self.time = QLabel(QDateTime.fromSecsSinceEpoch(int(ts or QDateTime.currentSecsSinceEpoch())).toString("yyyy-MM-dd hh:mm"))
        self.time.setStyleSheet("color:#9aa")
        self.copy = QPushButton("⧉"); self.copy.setFixedWidth(28)
        self.copy.setStyleSheet("QPushButton{background:#2e2e2e;border-radius:8px;padding:2px;color:#ddd}")
        self.copy.clicked.connect(self._copy)
        row.addWidget(self.time, 1, Qt.AlignmentFlag.AlignLeft)
        row.addWidget(self.copy, 0, Qt.AlignmentFlag.AlignRight)
        inner.addLayout(row)
        wrap.addWidget(frame, 0, Qt.AlignmentFlag.AlignLeft if role=="user" else Qt.AlignmentFlag.AlignRight)
    def _copy(self):
        QApplication.clipboard().setText(self.body.text())
