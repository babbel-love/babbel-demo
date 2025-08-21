from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal, QSettings

@dataclass
class SessionSnapshot:
    show_metadata: bool

class SessionState(QObject):

    def __init__(self) -> None:
        super().__init__()
        self._settings = QSettings("Babbel", "BabbelApp")
        self._show_metadata = bool(self._settings.value("session/show_metadata", True, type=bool))

    @property

    def show_metadata(self) -> bool:
        return self._show_metadata

    def set_show_metadata(self, on: bool) -> None:
        if self._show_metadata == on:
            return
        self._show_metadata = on
        self._settings.setValue("session/show_metadata", on)
        self.metadataToggled.emit(on)
        self.snapshotChanged.emit(self.snapshot())

    def snapshot(self) -> SessionSnapshot:
        return SessionSnapshot(show_metadata=self._show_metadata)

    @classmethod
    def instance(cls) -> "SessionState":
        if cls._instance is None:
            cls._instance = SessionState()
        return cls._instance
