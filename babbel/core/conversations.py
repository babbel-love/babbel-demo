from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from uuid import uuid4
from datetime import datetime, timezone
import json, os
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal, QSettings

# ---------- Models ----------

@dataclass
class Conversation:
    id: str
    title: str
    created_at: str
    messages_count: int = 0

@dataclass
class Message:
    id: str
    role: str            # "user" | "assistant" | "system"
    text: str
    emotions: Optional[Dict[str, float]]  # None or dict of emotion->score
    created_at: str

# ---------- Store ----------

class ConversationStore(QObject):
    listChanged = pyqtSignal(list)       # list of conversations (dicts)
    currentChanged = pyqtSignal(object)  # current conversation (dict) or None
    messageAppended = pyqtSignal(object) # appended message (dict) for current conv

    _instance: Optional["ConversationStore"] = None

    def __init__(self) -> None:
        super().__init__()
        self._settings = QSettings("Babbel", "BabbelApp")
        self._list: List[Conversation] = self._load_list()
        self._current_id: Optional[str] = self._settings.value("conversations/current_id", None, type=str)
        if self._current_id and not any(c.id == self._current_id for c in self._list):
            self._current_id = None
        if self._current_id is None and self._list:
            self._current_id = self._list[0].id

        # storage folder (macOS-friendly; still works elsewhere)
        self._base_dir = Path.home() / "Library" / "Application Support" / "Babbel" / "Conversations"
        try:
            self._base_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    @classmethod
    def instance(cls) -> "ConversationStore":
        if cls._instance is None:
            cls._instance = ConversationStore()
        return cls._instance

    # ----- Conversations list (QSettings) -----

    def _load_list(self) -> List[Conversation]:
        raw = self._settings.value("conversations/list_json", "[]", type=str)
        try:
            data = json.loads(raw)
            return [Conversation(**item) for item in data]
        except Exception:
            return []

    def _save_list(self) -> None:
        data = [asdict(c) for c in self._list]
        self._settings.setValue("conversations/list_json", json.dumps(data))

    def _emit_list(self) -> None:
        self.listChanged.emit([asdict(c) for c in self._list])

    def _emit_current(self) -> None:
        self.currentChanged.emit(self.current())

    def list(self) -> List[Conversation]:
        return list(self._list)

    def current(self) -> Optional[Conversation]:
        for c in self._list:
            if c.id == self._current_id:
                return c
        return None

    def new_conversation(self, title: str = "New Chat") -> Conversation:
        c = Conversation(id=str(uuid4()), title=title, created_at=self._now_iso())
        self._list.insert(0, c)
        self._current_id = c.id
        self._save_list()
        self._settings.setValue("conversations/current_id", self._current_id)
        # create an empty message file
        self._save_messages(c.id, [])
        self._emit_list()
        self._emit_current()
        return c

    def set_current(self, conv_id: str) -> None:
        if self._current_id == conv_id:
            return
        if not any(c.id == conv_id for c in self._list):
            return
        self._current_id = conv_id
        self._settings.setValue("conversations/current_id", self._current_id)
        self._emit_current()

    def rename(self, conv_id: str, title: str) -> None:
        for c in self._list:
            if c.id == conv_id:
                c.title = title
                break
        self._save_list()
        self._emit_list()
        if conv_id == self._current_id:
            self._emit_current()

    # ----- Messages (JSON per conversation) -----

    def append_message(self, role: str, text: str, emotions: Optional[Dict[str, float]]) -> Message:
        conv = self.current()
        if conv is None:
            conv = self.new_conversation()

        msgs = self._load_messages(conv.id)
        m = Message(
            id=str(uuid4()),
            role=role,
            text=text,
            emotions=emotions,
            created_at=self._now_iso()
        )
        msgs.append(asdict(m))
        self._save_messages(conv.id, msgs)

        # update counters & maybe title
        for c in self._list:
            if c.id == conv.id:
                c.messages_count += 1
                if c.messages_count == 1 and role == "user" and text.strip():
                    c.title = text.strip()[:60]
                break
        self._save_list()
        self._emit_list()
        self.messageAppended.emit(asdict(m))
        return m

    def load_current_messages(self) -> List[Dict[str, Any]]:
        conv = self.current()
        if conv is None:
            return []
        return self._load_messages(conv.id)

    # ----- File helpers -----

    def _conv_path(self, conv_id: str) -> Path:
        return self._base_dir / f"{conv_id}.json"

    def _load_messages(self, conv_id: str) -> List[Dict[str, Any]]:
        p = self._conv_path(conv_id)
        if not p.exists():
            return []
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _save_messages(self, conv_id: str, msgs: List[Dict[str, Any]]) -> None:
        p = self._conv_path(conv_id)
        try:
            p.write_text(json.dumps(msgs, ensure_ascii=False, indent=0), encoding="utf-8")
        except Exception:
            # fallback to settings if disk fails
            key = f"conversations/{conv_id}/messages_json"
            self._settings.setValue(key, json.dumps(msgs))

    # ----- Utils -----

    def record_message_for_legacy_title(self, is_user: bool, text: str) -> None:
        """Back-compat for code that only wanted to bump count and maybe title."""
        for c in self._list:
            if c.id == self._current_id:
                c.messages_count += 1
                if c.messages_count == 1 and is_user and text.strip():
                    c.title = text.strip()[:60]
                break
        self._save_list()
        self._emit_list()

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
