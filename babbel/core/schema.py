from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional
from datetime import datetime, timezone

def validate_timestamp(ts: Any) -> datetime:
    if isinstance(ts, datetime):
        return ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc)
    if not isinstance(ts, str):
        raise TypeError("timestamp must be string or datetime")
    s = ts.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+0000"
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M%z",
        "%Y-%m-%d %H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ]
    last = None
    for f in formats:
        try:
            dt = datetime.strptime(s, f)
            return dt.replace(tzinfo=timezone.utc) if "%z" not in f else dt
        except Exception as e:
            last = e
    raise ValueError(f"invalid timestamp: {ts}") from last

@dataclass
class UXBlock:
    thoughts: str
    reflection: str
    tips: Optional[str] = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "thoughts": self.thoughts,
            "reflection": self.reflection,
            "tips": self.tips or "",
        }

def standard_payload(
    sentiment: str = "neutral",
    ux: Optional[UXBlock] = None,
    culture_shift: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "sentiment": sentiment,
        "ux": ux.to_dict() if ux else UXBlock("","").to_dict(),
        "culture_shift": culture_shift,
        "metadata": metadata or {},
    }
