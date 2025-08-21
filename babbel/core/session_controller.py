from PyQt6.QtCore import QObject, pyqtSlot
from .session_state import SessionState

class SessionController(QObject):
    """Thin layer of slots you can connect UI buttons to."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.state = SessionState.instance()

    @pyqtSlot(bool)
    def toggle_metadata(self, checked: bool) -> None:
        self.state.set_show_metadata(checked)
