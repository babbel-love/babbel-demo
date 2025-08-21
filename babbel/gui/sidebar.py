from __future__ import annotations
from typing import Optional
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QSizePolicy

from babbel.conversations import ConversationStore

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.store = ConversationStore.instance()

        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(8)

        self.btnNew = QPushButton("New Chat", self)
        self.btnNew.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btnNew.clicked.connect(self._on_new_chat)
        root.addWidget(self.btnNew)

        self.list = QListWidget(self)
        self.list.itemSelectionChanged.connect(self._on_select)
        root.addWidget(self.list)

        self._refresh_list()
        self.store.listChanged.connect(lambda _: self._refresh_list())
        self.store.currentChanged.connect(lambda _: self._select_current())

        self.setFixedWidth(240)

    def _on_new_chat(self):
        self.store.new_conversation()

    def _on_select(self):
        items = self.list.selectedItems()
        if not items:
            return
        conv_id = items[0].data(Qt.ItemDataRole.UserRole)
        self.store.set_current(conv_id)

    def _refresh_list(self):
        self.list.clear()
        for conv in self.store.list():
            item = QListWidgetItem(f"{conv.title}")
            item.setData(Qt.ItemDataRole.UserRole, conv.id)
            self.list.addItem(item)
        self._select_current()

    def _select_current(self):
        cur = self.store.current()
        if not cur:
            return
        for i in range(self.list.count()):
            it = self.list.item(i)
            if it.data(Qt.ItemDataRole.UserRole) == cur.id:
                self.list.setCurrentItem(it)
                break
