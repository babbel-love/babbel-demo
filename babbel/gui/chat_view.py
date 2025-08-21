from __future__ import annotations
from typing import Dict, Optional, List
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from babbel.core.session_state import SessionState
from babbel.core.conversations import ConversationStore
from .chat_bubbles import MessageBubble

class ChatView(QWidget):
    """Scrollable vertical list of MessageBubble widgets with persistence."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = SessionState.instance()
        self.conversations = ConversationStore.instance()

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(self.scroll.Shape.NoFrame)

        self.container = QWidget(self.scroll)
        from PyQt6.QtWidgets import QVBoxLayout as _QVBoxLayout
        self.vbox = _QVBoxLayout(self.container)
        self.vbox.setContentsMargins(12, 12, 12, 12)
        self.vbox.setSpacing(8)
        self.vbox.addStretch(1)

        self.scroll.setWidget(self.container)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(self.scroll)

        self.state.snapshotChanged.connect(self._apply_state)
        self.conversations.currentChanged.connect(self._on_conversation_changed)

        self._bubbles: list[MessageBubble] = []
        self._loading = False

        # initial load
        self._on_conversation_changed(self.conversations.current())

    def add_message(self, role: str, text: str, emotions: Optional[Dict[str, float]] = None) -> MessageBubble:
        bubble = MessageBubble(
            role=role,
            text=text,
            emotions=emotions if role == "assistant" else None,
            show_metadata=self.state.show_metadata,
            parent=self.container
        )
        self.vbox.insertWidget(self.vbox.count() - 1, bubble, alignment=Qt.AlignmentFlag.AlignLeft if role == "assistant" else Qt.AlignmentFlag.AlignRight)
        self._bubbles.append(bubble)
        self._scroll_to_bottom()

        # Persist (skip while bulk-loading)
        if not self._loading:
            self.conversations.append_message(role=role, text=text, emotions=emotions if role=="assistant" else None)

        return bubble

    def clear_chat(self) -> None:
        for b in self._bubbles:
            b.setParent(None)
            b.deleteLater()
        self._bubbles.clear()

    def _apply_state(self, snap) -> None:
        for b in self._bubbles:
            b.set_show_metadata(snap.show_metadata)

    def _scroll_to_bottom(self) -> None:
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

    def _on_conversation_changed(self, conv):
        # Load messages for selected conversation
        self.clear_chat()
        if conv is None:
            return
        msgs = self.conversations.load_current_messages()
        self._loading = True
        try:
            for m in msgs:
                role = m.get("role","assistant")
                text = m.get("text","")
                emotions = m.get("emotions")
                self.add_message(role, text, emotions=emotions)
        finally:
            self._loading = False
