from __future__ import annotations
from typing import Dict, Any
from babbel.core.prompt_builder import build_messages

class IdentityLock:
    def __init__(self) -> None:
        self._last_messages = None

    def build_messages(self, *, anchor: str, user_text: str) -> Any:
        self._last_messages = build_messages(user_input=user_text, system_prompt="# Babbel Protocol (Enforced)")
        return self._last_messages

    def send(self, *, anchor: str, user_text: str) -> Dict[str, Any]:
        if not anchor or not isinstance(anchor, str):
            raise ValueError("Anchor required")
        messages = self.build_messages(anchor=anchor, user_text=user_text)
        return {"ok": True, "messages": messages}
