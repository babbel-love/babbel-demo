import json
import os
import uuid
from typing import List, Dict, Any

class ConversationThread:
    def __init__(self, thread_name: str, model: str, temperature: float, memory_messages_number: int):
        self.thread_name: str = thread_name
        self.model: str = model
        self.temperature: float = float(temperature)
        self.memory_messages_number: int = int(memory_messages_number)
        self.messages: List[Dict[str, Any]] = []
        self.thread_id: str = uuid.uuid4().hex

    def add_message(self, role: str, text: str) -> None:
        self.messages.append({"role": role, "content": str(text)})

    def add_multimodal_message(self, role: str, text: str, image_data_list: List[str]) -> None:
        parts: List[Dict[str, Any]] = [{"type": "image_url", "image_url": {"url": url}} for url in image_data_list]
        parts.append({"type": "text", "text": str(text)})
        self.messages.append({"role": role, "content": parts})

    def to_dict(self) -> Dict[str, Any]:
        return {
            "thread_name": self.thread_name,
            "model": self.model,
            "temperature": self.temperature,
            "memory_messages_number": self.memory_messages_number,
            "messages": self.messages,
            "thread_id": self.thread_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationThread":
        obj = cls(
            data.get("thread_name", "Untitled"),
            data.get("model", "babbel-local/deterministic"),
            data.get("temperature", 0.0),
            data.get("memory_messages_number", 10),
        )
        obj.messages = data.get("messages", [])
        obj.thread_id = data.get("thread_id") or obj.thread_id
        return obj

    def save(self, directory: str) -> None:
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, f"{self.thread_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str) -> "ConversationThread":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
