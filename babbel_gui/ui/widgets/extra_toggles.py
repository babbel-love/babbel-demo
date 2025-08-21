from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from PyQt6.QtCore import pyqtSignal

class ExtraToggles(QWidget):
    togglesChanged = pyqtSignal(dict)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.boxes = {
            "emotion_savvy": QCheckBox("Emotion Savvy"),
            "emit_emotion_series": QCheckBox("Emotion Tracker"),
            "cultural_sensitivity": QCheckBox("Cultural Sensitivity"),
        }
        lay = QVBoxLayout(self)
        [lay.addWidget(b) for b in self.boxes.values()]
        [b.stateChanged.connect(self._emit) for b in self.boxes.values()]
    def state(self): return {k: b.isChecked() for k,b in self.boxes.items()}
    def _emit(self,*_): self.togglesChanged.emit(self.state())
