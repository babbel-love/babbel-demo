"""
emotion_scorebar.py
Exports:
- score_emotions(text: str) -> dict[str, float]
"""
from __future__ import annotations
import re
from typing import Dict

_EMOTION_KEYWORDS = {
    "shame": ["worthless", "ashamed", "disgust", "humiliated", "embarrassed"],
    "grief": ["loss", "heartbroken", "mourning", "miss", "sad"],
    "anger": ["angry", "rage", "furious", "fed up", "annoyed"],
    "fear": ["scared", "afraid", "anxious", "worried", "panic"],
    "wonder": ["curious", "what if", "imagine", "open to", "explore"],
    "joy": ["happy", "grateful", "excited", "relieved", "love"],
}

def score_emotions(text: str) -> Dict[str, float]:
    t = (text or "").lower()
    raw = {emo: 0 for emo in _EMOTION_KEYWORDS}
    for emo, keys in _EMOTION_KEYWORDS.items():
        for k in keys:
            if re.search(r"\b" + re.escape(k) + r"\b", t):
                raw[emo] += 1
    total = sum(raw.values())
    if total <= 0:
        return {emo: 0.0 for emo in raw}
    return {emo: round(cnt / total, 2) for emo, cnt in raw.items()}

__all__ = ["score_emotions"]
