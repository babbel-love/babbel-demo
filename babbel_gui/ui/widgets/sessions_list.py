from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel
from PyQt6.QtCore import pyqtSignal
import os, glob

class SessionsList(QWidget):
    sessionChosen = pyqtSignal(str)
    def __init__(self, root_dir: str, parent=None):
        super().__init__(parent)
        self._dir = os.path.expanduser(root_dir)
        lay = QVBoxLayout(self); lay.setContentsMargins(0,0,0,0); lay.setSpacing(6)
        lay.addWidget(QLabel("Sessions"))
        self.list = QListWidget(self); lay.addWidget(self.list)
        self.list.itemDoubleClicked.connect(self._emit_path)
        self.refresh()
    def refresh(self):
        os.makedirs(self._dir, exist_ok=True)
        self.list.clear()
        files = sorted(glob.glob(os.path.join(self._dir, "*.json")), key=os.path.getmtime, reverse=True)
        for f in files:
            self.list.addItem(os.path.basename(f))
    def _emit_path(self, item):
        self.sessionChosen.emit(os.path.join(self._dir, item.text()))
