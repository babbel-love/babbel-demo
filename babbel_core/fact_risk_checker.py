"""
fact_risk_checker.py
Lightweight heuristics to flag user prompts that likely require fact verification
(recency, numbers, claims about people/places/events, or strong certainty language).

Exports:
- detect_fact_risk(text: str) -> dict
- requires_web_validation(text: str) -> bool
"""
from __future__ import annotations
import re
from typing import Dict, List

_RECENCY = (
    "today","yesterday","tomorrow","this week","last week","next week",
    "this month","last month","next month","currently","as of","latest",
    "breaking","update","recent","now","right now","live"
)
_CERTAINTY = (
    "definitely","proven","confirmed","always","never",
    "undeniably","for sure","no doubt","guaranteed"
)
_ENTITY_HINTS = (
    "president","ceo","prime minister","minister","governor","mayor",
    "price","stock","rate","unemployment","inflation",
    "earnings","revenue","forecast","release date","launch",
    "schedule","score","result","deadline","law","bill","policy",
    "airport","flight","train","concert","festival"
)

_NUM_PATTERN = re.compile(r"\b\d{1,3}(?:[,\s]\d{3})*(?:\.\d+)?\b")
_DATE_PATTERN = re.compile(
    r"\b(?:\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})|"
    r"jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec|"
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
    flags=re.IGNORECASE,
)

def _find_flags(text: str) -> List[str]:
    t = (text or "").lower()
    flags: List[str] = []
    recency_hits = [w for w in _RECENCY if w in t]
    flags.extend(sorted(set(recency_hits)))
    if _NUM_PATTERN.search(t):
        flags.append("number")
    if _DATE_PATTERN.search(t):
        flags.append("date/time")
    entity_hits = [w for w in _ENTITY_HINTS if w in t]
    flags.extend(sorted(set(entity_hits)))
    cert_hits = [w for w in _CERTAINTY if w in t]
    flags.extend(sorted(set(cert_hits)))
    if any(k in t for k in ("who is","who’s","who was","what is","what’s","when is","when’s")):
        flags.append("explicit fact query")
    return sorted(set(flags))

def _score_from_flags(flags: List[str]) -> float:
    if not flags: return 0.0
    score = 0.15
    if "number" in flags: score += 0.25
    if "date/time" in flags: score += 0.20
    if any(f in flags for f in _RECENCY): score += 0.25
    if any(f in flags for f in _ENTITY_HINTS): score += 0.15
    if any(f in flags for f in _CERTAINTY): score += 0.10
    return max(0.0, min(1.0, score))

def _bucket(score: float) -> str:
    if score >= 0.7: return "high"
    if score >= 0.35: return "medium"
    return "low"

def detect_fact_risk(text: str) -> Dict[str, object]:
    flags = _find_flags(text)
    score = _score_from_flags(flags)
    bucket = _bucket(score)
    if not flags:
        notes = "No obvious factual risk indicators."
    elif bucket == "high":
        notes = "Time-sensitive or numeric claim; verify with live sources."
    elif bucket == "medium":
        notes = "Some factual indicators present; consider verification."
    else:
        notes = "Low-risk, but skim for outdated specifics."
    return {"risk": bucket, "score": round(score, 2), "flags": flags, "notes": notes}

def requires_web_validation(text: str) -> bool:
    return detect_fact_risk(text).get("risk") in ("medium","high")

__all__ = ["detect_fact_risk","requires_web_validation"]
