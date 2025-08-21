from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
class Toast(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background:#333;color:#fff;border-radius:8px;padding:6px;")
        lay = QHBoxLayout(self); self._lbl = QLabel(""); lay.addWidget(self._lbl)
        self.hide()
    def show_msg(self, text, ms=2000):
        self._lbl.setText(text); self.show(); QTimer.singleShot(ms, self.hide)
