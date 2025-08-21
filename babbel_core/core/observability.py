from __future__ import annotations
import json, uuid, time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

def new_trace_id() -> str:
    return uuid.uuid4().hex

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class jsonl_logger:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
    def write(self, obj: Dict[str, Any]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

@contextmanager
def time_block(_name: str = ""):
    start = time.perf_counter()
    data: Dict[str, Any] = {}
    try:
        yield data
    finally:
        data["elapsed_ms"] = int((time.perf_counter() - start) * 1000)
