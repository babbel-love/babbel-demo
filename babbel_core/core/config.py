from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass
class Config:
    MEMORY_FILE: str
    LOG_JSONL: str
    CONTEXT_ITEMS: int
    MAX_LINES: int
    STYLE_PROFILE: str
    MODEL_NAME: str
    TIMEOUT_S: int

def _int_env(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, str(default)))
    except Exception:
        return default

def load() -> Config:
    return Config(
        MEMORY_FILE=os.environ.get("BABBEL_MEMORY_FILE", "memory_log.json"),
        LOG_JSONL=os.environ.get("BABBEL_LOG_JSONL", "events.jsonl"),
        CONTEXT_ITEMS=_int_env("BABBEL_CONTEXT_ITEMS", 6),
        MAX_LINES=_int_env("BABBEL_MAX_LINES", 6),
        STYLE_PROFILE=os.environ.get("BABBEL_STYLE", "warm_coach"),
        MODEL_NAME=os.environ.get("BABBEL_MODEL", "openrouter/fallback"),
        TIMEOUT_S=_int_env("BABBEL_TIMEOUT_S", 20),
    )
