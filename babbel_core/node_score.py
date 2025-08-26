"""
node_score.py
Lightweight, deterministic node scoring for Babbel.

Exports:
- score_node(text: str, emotion: str|None = None, intent: str|None = None, fact_flags: list[str]|None = None) -> dict
- score_confidence(text: str) -> float
"""

from __future__ import annotations
import re
from typing import List, Dict, Optional

# Basic keyword buckets that reflect therapeutic utility/risk
POSITIVE_CUES = (
    "i can", "willing", "curious", "open to", "try", "learn", "notice", "aware", "choice", "agency"
)
RUMINATION_CUES = (
    "always", "never", "should", "must", "why me", "what's wrong with me", "i can't", "hopeless", "worthless"
)
RISK_CUES = (
    "suicide", "kill myself", "end it", "self-harm", "cutting", "overdose"
)

INTENT_WEIGHTS = {
    "seek guidance": 0.10,
    "search for meaning": 0.12,
    "confession": 0.08,
    "protest": 0.06,
    "explore": 0.09,
}

EMOTION_WEIGHTS = {
    "shame": -0.08,
    "grief": -0.04,
    "anger": -0.02,
    "fear": -0.05,
    "wonder": +0.06,
    "mixed": 0.00,
}

def _contains_any(text: str, terms: tuple[str, ...]) -> int:
    t = text.lower()
    return sum(1 for w in terms if w in t)

def score_confidence(text: str) -> float:
    """
    Proxy for 'how specific and confident is this message'.
    Heuristics: punctuation, numbers, and reduction of hedges.
    Returns 0.0–1.0
    """
    t = (text or "").strip()
    if not t:
        return 0.0
    length = len(t.split())
    length_term = min(1.0, max(0.0, (length - 3) / 40.0))  # saturate around ~43 words

    # Specificity: numbers / concrete refs
    has_number = bool(re.search(r"\d", t))
    has_colon  = ":" in t
    has_quotes = '"' in t or "'" in t
    spec = 0.15 * has_number + 0.05 * has_colon + 0.05 * has_quotes

    # Less hedging -> higher confidence
    hedges = len(re.findall(r"\b(just|maybe|perhaps|sort of|kinda|i think|it seems)\b", t, flags=re.I))
    hedge_penalty = min(0.3, hedges * 0.08)

    conf = max(0.0, min(1.0, 0.35 + length_term + spec - hedge_penalty))
    return round(conf, 2)

def score_node(
    text: str,
    emotion: Optional[str] = None,
    intent: Optional[str] = None,
    fact_flags: Optional[List[str]] = None
) -> Dict[str, object]:
    """
    Returns a structured score block the pipeline can attach to metadata.

    {
      "score": 0.62,                    # overall utility score (0–1)
      "risk": 0.18,                     # risk (0–1)
      "confidence": 0.71,               # reply confidence (0–1)
      "signals": { ... },               # raw signal counts
      "reasons": [ ... ]                # short human-readable rationales
    }
    """
    msg = (text or "").strip()
    reasons: List[str] = []
    signals: Dict[str, int] = {}

    pos_hits  = _contains_any(msg, POSITIVE_CUES)
    rum_hits  = _contains_any(msg, RUMINATION_CUES)
    risk_hits = _contains_any(msg, RISK_CUES)

    signals["positive_cues"]  = pos_hits
    signals["rumination"]     = rum_hits
    signals["self_harm_risk"] = risk_hits

    # Base utility score from cues
    score = 0.5
    score += min(0.25, pos_hits * 0.06)
    score -= min(0.30, rum_hits * 0.07)

    if pos_hits:
        reasons.append("Signs of agency/curiosity present.")
    if rum_hits:
        reasons.append("Globalizing/ruminative language detected.")
    if risk_hits:
        reasons.append("Self-harm risk cues present — elevate safety checks.")

    # Intent / emotion shaping
    if intent:
        score += INTENT_WEIGHTS.get(intent, 0.0)
        reasons.append(f"Intent: {intent}.")
    if emotion:
        score += EMOTION_WEIGHTS.get(emotion, 0.0)
        reasons.append(f"Emotion: {emotion}.")

    # Fact risk slightly reduces utility (needs verification)
    ff = tuple(sorted(set(fact_flags or [])))
    if ff:
        score -= min(0.10, 0.03 * len(ff))
        reasons.append(f"Fact-check flags: {', '.join(ff)}.")

    # Clamp score 0–1
    score = max(0.0, min(1.0, score))

    # Risk channel: self-harm cues dominate; otherwise mild from rumination
    risk = 0.0
    if risk_hits:
        risk = 0.85 if risk_hits >= 2 else 0.65
    elif rum_hits:
        risk = min(0.35, 0.12 + rum_hits * 0.06)

    confidence = score_confidence(msg)

    return {
        "score": round(score, 2),
        "risk": round(risk, 2),
        "confidence": confidence,
        "signals": signals,
        "reasons": reasons,
    }

__all__ = ["score_node", "score_confidence"]
