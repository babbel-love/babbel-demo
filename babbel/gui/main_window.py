from __future__ import annotations
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from babbel.core.session_state import SessionState
from babbel.core.session_controller import SessionController
from babbel.core.conversations import ConversationStore
from babbel.gui.chat_view import ChatView
from babbel.gui.sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        try:
            with open('babbel/gui/styles.qss','r',encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass

        self.state = SessionState.instance()
        self.controller = SessionController(self)
        self.conversations = ConversationStore.instance()
        if self.conversations.current() is None and not self.conversations.list():
            self.conversations.new_conversation()

        top_bar = QWidget(self)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(12, 12, 12, 6)

        title = QLabel("Babbel")
        title.setStyleSheet("font-size: 16px; font-weight: 600;")
        top_layout.addWidget(title)

        top_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.btnNewChat = QPushButton("New Chat", top_bar)
        self.btnNewChat.setToolTip("Start a new conversation")
        self.btnNewChat.clicked.connect(lambda: self.conversations.new_conversation())
        top_layout.addWidget(self.btnNewChat)

        self.btnMetadata = QPushButton("Metadata", top_bar)
        self.btnMetadata.setCheckable(True)
        self.btnMetadata.setChecked(self.state.show_metadata)
        self.btnMetadata.setToolTip("Show/Hide message metadata")
        self._apply_toggle_style(self.btnMetadata, self.btnMetadata.isChecked())
        self.btnMetadata.toggled.connect(self.controller.toggle_metadata)
        self.state.metadataToggled.connect(lambda on: self._apply_toggle_style(self.btnMetadata, on))
        self.state.metadataToggled.connect(self.btnMetadata.setChecked)
        top_layout.addWidget(self.btnMetadata)

        body = QWidget(self)
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(0,0,0,0)
        body_layout.setSpacing(0)
        body_layout.addWidget(top_bar)

        center = QWidget(self)
        center_layout = QHBoxLayout(center)
        center_layout.setContentsMargins(0,0,0,0)
        center_layout.setSpacing(0)

        self.sidebar = Sidebar(center)
        center_layout.addWidget(self.sidebar)

        self.chat_view = ChatView(center)
        center_layout.addWidget(self.chat_view, 1)

        body_layout.addWidget(center, 1)
        self.setCentralWidget(body)

        self.state.snapshotChanged.connect(self._on_snapshot_changed)
        self._on_snapshot_changed(self.state.snapshot())

    def _on_snapshot_changed(self, snap) -> None:
        pass

    def _apply_toggle_style(self, btn: QPushButton, on: bool) -> None:
        if on:
            btn.setStyleSheet("""
                QPushButton { 
                    border-radius: 14px; padding: 6px 12px; 
                    background: #10a37f; color: white; font-weight: 600;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton { 
                    border-radius: 14px; padding: 6px 12px; 
                    background: #2f2f2f; color: #cfcfcf; 
                }
            """)