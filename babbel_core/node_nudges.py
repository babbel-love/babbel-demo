"""
node_nudges.py
Deterministic micro‑nudges for Babbel keyed by (emotion, intent) + text cues.

Exports:
- get_nudges(text: str, emotion: str | None, intent: str | None) -> list[str]
- pick_nudges(text: str, emotion: str | None, intent: str | None, k: int = 2) -> list[str]
"""
from __future__ import annotations
import re
from typing import List, Dict, Tuple, Optional

# Base library of short, concrete prompts that move the user one notch.
# Keys are (emotion, intent) both lowercased.
NUDGES: Dict[Tuple[str, str], List[str]] = {
    ("shame", "search for meaning"): [
        "What exactly feels 'wrong' about you right now—say it in one plain sentence.",
        "If a friend said this about themselves, what would you notice first?"
    ],
    ("shame", "seek guidance"): [
        "Name one thing you did today that wasn’t about being 'good'—just about being you.",
        "Where in your body does shame land first? Describe the sensation, not the story."
    ],
    ("grief", "search for meaning"): [
        "What part of you is most changed by this loss?",
        "If love could speak here, what would it thank you for carrying?"
    ],
    ("grief", "seek guidance"): [
        "Pick one small ritual to honor what mattered. Try it this week.",
        "Who can witness this with you for five quiet minutes?"
    ],
    ("anger", "explore"): [
        "What boundary was crossed? Name it without apology.",
        "What would 'clean anger' sound like in one sentence?"
    ],
    ("fear", "seek guidance"): [
        "List two steps small enough to do while afraid.",
        "If you were 10% braver, what would you try tonight?"
    ],
    ("wonder", "explore"): [
        "Follow the spark: what’s a 24‑hour experiment you can run?",
        "What would make this curiosity easier to revisit tomorrow?"
    ],
    ("mixed", "confession"): [
        "If you didn’t fix anything, what truth would you want seen first?",
        "Say it plain, no spin: what actually happened?"
    ],
}

# Cue-based additions (regex -> nudges). Keep short, zero fluff, specific.
CUE_NUDGES: List[Tuple[re.Pattern, List[str]]] = [
    (re.compile(r"\bworthless|broken|defective\b", re.I), [
        "What evidence are you using for that verdict? List two items, then test them."
    ]),
    (re.compile(r"\balways|never\b", re.I), [
        "Trade 'always/never' for a time window: when exactly did this happen last?"
    ]),
    (re.compile(r"\bshould\b", re.I), [
        "Replace one 'should' with a choice: what do you actually want here?"
    ]),
    (re.compile(r"\boverwhelmed|panic|anxious|worried\b", re.I), [
        "Name 3 things in the room. Feel your feet. Then one tiny step you can actually do."
    ]),
    # Safety: provide supportive direction if self-harm terms appear
    (re.compile(r"\b(ending it|end it|suicide|kill myself|self[- ]?harm)\b", re.I), [
        "If you’re in danger right now, please call your local emergency number or a crisis line. You matter."
    ]),
]

def _base_nudges(emotion: Optional[str], intent: Optional[str]) -> List[str]:
    key = ((emotion or "mixed").lower(), (intent or "explore").lower())
    return list(NUDGES.get(key, []))

def _cue_nudges(text: str) -> List[str]:
    t = text or ""
    out: List[str] = []
    for pat, adds in CUE_NUDGES:
        if pat.search(t):
            out.extend(adds)
    # De‑dup while preserving order
    seen = set()
    uniq: List[str] = []
    for n in out:
        if n not in seen:
            seen.add(n)
            uniq.append(n)
    return uniq

def get_nudges(text: str, emotion: Optional[str] = None, intent: Optional[str] = None) -> List[str]:
    """
    Returns a list of nudges combining (emotion,intent) and text cue matches.
    Deterministic order: base nudges first, then cue nudges, de‑duplicated.
    """
    base = _base_nudges(emotion, intent)
    cues = _cue_nudges(text or "")
    seen = set()
    out: List[str] = []
    for n in base + cues:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out

def pick_nudges(text: str, emotion: Optional[str] = None, intent: Optional[str] = None, k: int = 2) -> List[str]:
    """Convenience picker that returns up to k nudges from get_nudges()."""
    return get_nudges(text, emotion, intent)[: max(0, k)]

__all__ = ["get_nudges", "pick_nudges"]
