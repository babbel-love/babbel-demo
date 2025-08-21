from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QFrame
from PyQt6.QtCore import pyqtSignal
from .widgets.extra_toggles import ExtraToggles
from .widgets.sessions_list import SessionsList

SESS_DIR = "~/Downloads/Babbel_Sessions"

class Sidebar(QWidget):
    metadataToggled  = pyqtSignal(bool)
    livePreviewToggled = pyqtSignal(bool)
    extraTogglesChanged = pyqtSignal(dict)
    sessionChosen = pyqtSignal(str)

    def __init__(self, *, show_metadata=True, live_preview=True, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self); lay.setContentsMargins(8,8,8,8); lay.setSpacing(8)

        lay.addWidget(QLabel("Controls"))        self._metadata    = QCheckBox("Show Metadata");    self._metadata.setChecked(show_metadata)
        self._livePreview = QCheckBox("Live Emotion Preview"); self._livePreview.setChecked(live_preview)        self._metadata.stateChanged.connect(lambda _: self.metadataToggled.emit(self._metadata.isChecked()))
        self._livePreview.stateChanged.connect(lambda _: self.livePreviewToggled.emit(self._livePreview.isChecked())); lay.addWidget(self._metadata); lay.addWidget(self._livePreview)

        line = QFrame(self); line.setFrameShape(QFrame.Shape.HLine); line.setFrameShadow(QFrame.Shadow.Sunken); lay.addWidget(line)

        lay.addWidget(QLabel("Experience"))
        self._extra = ExtraToggles(self); self._extra.togglesChanged.connect(self.extraTogglesChanged.emit); lay.addWidget(self._extra)

        line2 = QFrame(self); line2.setFrameShape(QFrame.Shape.HLine); line2.setFrameShadow(QFrame.Shadow.Sunken); lay.addWidget(line2)

        self._sessions = SessionsList(SESS_DIR, self)
        self._sessions.sessionChosen.connect(self.sessionChosen.emit)
        lay.addWidget(self._sessions)

    def refreshSessions(self):
        self._sessions.refresh()
