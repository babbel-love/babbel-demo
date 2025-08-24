from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .config import load

@dataclass
class Profile:
    name: str
    max_lines: int

def from_config(cfg=None) -> Profile:
    cfg = cfg or load()
    return Profile(name=str(getattr(cfg, "STYLE_PROFILE", "warm_coach")), max_lines=int(getattr(cfg, "MAX_LINES", 6)))

def apply(text: str, profile: Profile) -> str:
    lines = [ln.rstrip() for ln in (text or "").strip().splitlines() if ln.strip()]
    return "\n".join(lines[: max(1, profile.max_lines)])
