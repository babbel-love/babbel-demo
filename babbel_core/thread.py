import json, os, uuid, time
from typing import List, Dict, Any, Optional
from utils import ensure_dir, safe_read_json, safe_write_json
from schema_validation import validate_thread_dict

class ConversationThread:
    def __init__(self, thread_name: str, model: str, temperature: float, memory_messages_number: int):
        self.thread_name: str = thread_name
        self.model: str = model
        self.temperature: float = float(temperature)
        self.memory_messages_number: int = int(memory_messages_number)
        self.messages: List[Dict[str, Any]] = []
        self.thread_id: str = uuid.uuid4().hex

    def add_message(self, role: str, text: str, meta: Optional[Dict[str, Any]] = None) -> None:
        entry: Dict[str, Any] = {"role": role, "content": str(text)}
        if meta:
            entry["meta"] = meta
        self.messages.append(entry)

    def add_multimodal_message(self, role: str, text: str, image_data_list: List[str], meta: Optional[Dict[str, Any]] = None) -> None:
        parts: List[Dict[str, Any]] = [{"type": "image_url", "image_url": {"url": url}} for url in image_data_list]
        parts.append({"type": "text", "text": str(text)})
        entry: Dict[str, Any] = {"role": role, "content": parts}
        if meta:
            entry["meta"] = meta
        self.messages.append(entry)

    def pop_last_exchange(self) -> None:
        if not self.messages:
            return
        # remove trailing non-user/assistant (unlikely)
        while self.messages and self.messages[-1].get("role") not in ("user","assistant"):
            self.messages.pop()
        if not self.messages:
            return
        # remove last assistant if present, else remove last message
        if self.messages[-1].get("role") == "assistant":
            self.messages.pop()
        # remove last user if present
        if self.messages and self.messages[-1].get("role") == "user":
            self.messages.pop()

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
            data.get("model", "openrouter/auto"),
            data.get("temperature", 0.0),
            data.get("memory_messages_number", 10),
        )
        obj.messages = data.get("messages", [])
        obj.thread_id = data.get("thread_id") or obj.thread_id
        return obj

    def save(self, directory: str) -> str:
        ensure_dir(directory)
        payload = self.to_dict()
        validate_thread_dict(payload)
        path = os.path.join(directory, f"{self.thread_id}.json")
        safe_write_json(path, payload)
        return path

    @classmethod
    def load(cls, path: str) -> "ConversationThread":
        data = safe_read_json(path, {})
        return cls.from_dict(data)

class SessionStore:
    def __init__(self, base_dir: str = "sessions"):
        self.base_dir = ensure_dir(base_dir)
        self.index_path = os.path.join(self.base_dir, "index.json")
        self._init_index()

    def _init_index(self) -> None:
        if not os.path.exists(self.index_path):
            safe_write_json(self.index_path, {"sessions": {}})

    def _read_index(self) -> Dict[str, Any]:
        return safe_read_json(self.index_path, {"sessions": {}})

    def _write_index(self, data: Dict[str, Any]) -> None:
        safe_write_json(self.index_path, data)

    def list_sessions(self) -> List[Dict[str, Any]]:
        data = self._read_index().get("sessions", {})
        rows = []
        for tid, meta in data.items():
            path = os.path.join(self.base_dir, f"{tid}.json")
            mtime = os.path.getmtime(path) if os.path.exists(path) else 0
            rows.append({
                "thread_id": tid,
                "name": meta.get("name") or "Untitled",
                "model": meta.get("model") or "openrouter/auto",
                "updated": int(mtime),
            })
        rows.sort(key=lambda r: r["updated"], reverse=True)
        return rows

    def search_sessions(self, query: str, deep: bool = False) -> List[Dict[str, Any]]:
        q = (query or "").lower().strip()
        rows = self.list_sessions()
        if not q:
            return rows
        base = [r for r in rows if q in r["name"].lower() or q in r["thread_id"].lower()]
        if not deep:
            return base
        # deep: check message contents
        seen = {r["thread_id"] for r in base}
        from typing import Set
        add: Set[str] = set()
        for r in rows:
            if r["thread_id"] in seen:
                continue
            try:
                t = self.load_thread(r["thread_id"])
            except Exception:
                continue
            for m in t.messages:
                c = m.get("content","")
                if not isinstance(c, str):
                    import json as _json
                    c = _json.dumps(c)
                if q in (c or "").lower():
                    add.add(r["thread_id"])
                    break
        return [r for r in rows if r["thread_id"] in seen.union(add)]

    def save_thread(self, thread: ConversationThread) -> str:
        if not thread.thread_name or thread.thread_name == "Untitled":
            first_user = ""
            for m in thread.messages:
                if m.get("role") == "user":
                    c = m.get("content", "")
                    first_user = c if isinstance(c, str) else str(c)
                    break
            title = (first_user.strip()[:60] or "New chat")
            thread.thread_name = title
        path = thread.save(self.base_dir)
        idx = self._read_index()
        idx.setdefault("sessions", {})[thread.thread_id] = {
            "name": thread.thread_name,
            "model": thread.model,
        }
        self._write_index(idx)
        return path

    def load_thread(self, thread_id: str) -> ConversationThread:
        path = os.path.join(self.base_dir, f"{thread_id}.json")
        return ConversationThread.load(path)

    def delete_thread(self, thread_id: str) -> None:
        path = os.path.join(self.base_dir, f"{thread_id}.json")
        if os.path.exists(path):
            os.remove(path)
        idx = self._read_index()
        if "sessions" in idx and thread_id in idx["sessions"]:
            del idx["sessions"][thread_id]
            self._write_index(idx)

    def rename_thread(self, thread_id: str, new_name: str) -> None:
        idx = self._read_index()
        sess = idx.get("sessions", {})
        if thread_id in sess:
            sess[thread_id]["name"] = (new_name or "Untitled").strip() or "Untitled"
            self._write_index(idx)
            path = os.path.join(self.base_dir, f"{thread_id}.json")
            if os.path.exists(path):
                t = ConversationThread.load(path)
                t.thread_name = sess[thread_id]["name"]
                t.save(self.base_dir)
