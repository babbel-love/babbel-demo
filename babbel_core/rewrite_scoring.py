# rewrite_scoring.py
# Message-level scoring + overlays (stdlib only)

from __future__ import annotations
import re, difflib
from typing import Dict, List

# Local deps (all optional, with safe fallbacks)
try:
    from emotion_classifier import classify_emotion
except Exception:
    def classify_emotion(t: str) -> str: return "mixed"

try:
    from intent_classifier import classify_intent
except Exception:
    def classify_intent(t: str) -> str: return "explore"

try:
    from node_rules import apply_node_rules
except Exception:
    def apply_node_rules(_text, _emotion=None, _intent=None): return "Let’s slow this down together and see what’s really here."

try:
    from rewrite import rewrite_tone, enforce_babbel_style
except Exception:
    def rewrite_tone(t: str) -> str: return t
    def enforce_babbel_style(t: str) -> str: return t

try:
    from memory_tracker import get_recent_emotions
except Exception:
    def get_recent_emotions(n=10): return []

FACT_FLAG_WORDS = ("latest", "today", "as of", "currently", "expected", "estimated", "about", "roughly")

def get_fact_flags(text: str) -> List[str]:
    flags = [w for w in FACT_FLAG_WORDS if w in text.lower()]
    if re.search(r"\d", text): flags.append("number")
    return sorted(set(flags))

_HEDGES = [
    r"\bjust\b", r"\bmaybe\b", r"\bperhaps\b", r"\bi think\b", r"\bit seems\b",
    r"\bi feel like\b", r"\bkinda\b", r"\bsort of\b"
]

_WEAK_MARKERS = [
    r"\bthere (is|are)\b",
    r"\bit is important to note that\b",
    r"\bshould\b",
    r"\butilize\b",
    r"\bcan be\b",
]

def _count_patterns(text: str, patterns: List[str]) -> int:
    t = text.lower()
    return sum(1 for pat in patterns if re.search(pat, t))

def rewrite_confidence(original_model_text: str, babbel_text: str) -> float:
    """Heuristic: score combines edit distance + removed hedges/weakness + length sanity."""
    if not babbel_text:
        return 0.0

    # 1) How much changed?
    ratio = difflib.SequenceMatcher(a=original_model_text.lower(), b=babbel_text.lower()).ratio()
    change = 1.0 - ratio  # more change -> higher score (up to a point)

    # 2) Did we remove hedges/weak phrasing?
    h_before = _count_patterns(original_model_text, _HEDGES) + _count_patterns(original_model_text, _WEAK_MARKERS)
    h_after  = _count_patterns(babbel_text, _HEDGES) + _count_patterns(babbel_text, _WEAK_MARKERS)
    reduction = max(0, h_before - h_after)
    style_bonus = min(0.4, 0.12 * reduction)  # capped bonus

    # 3) Penalize if rewrite became too short
    len_before = max(1, len(original_model_text.strip()))
    len_after  = max(1, len(babbel_text.strip()))
    length_ratio = len_after / float(len_before)
    too_short_penalty = 0.0
    if length_ratio < 0.45:
        too_short_penalty = 0.25
    elif length_ratio < 0.65:
        too_short_penalty = 0.10

    raw = 0.45 * change + style_bonus - too_short_penalty
    return max(0.0, min(1.0, raw))

def node_influence_breakdown(user_text: str) -> Dict:
    emo = classify_emotion(user_text)
    intent = classify_intent(user_text)

    # Simple weighting rule-of-thumb
    weights = {"emotion": 0.6, "intent": 0.4}
    nudge = apply_node_rules(user_text, emo, intent)

    explanation = (
        f"Emotion={emo} (60%) and Intent={intent} (40%) shaped the rewrite. "
        f"Nudge: {nudge}"
    )
    return {"emotion": emo, "intent": intent, "weights": weights, "nudge": nudge, "explanation": explanation}

def memory_heatmap() -> List[Dict[str, float]]:
    recent = get_recent_emotions(30) or []
    if not recent:
        return []
    counts: Dict[str, int] = {}
    for e in recent:
        counts[e] = counts.get(e, 0) + 1
    total = sum(counts.values()) or 1
    return [{"label": k, "weight": round(v/total, 3)} for k, v in sorted(counts.items(), key=lambda x: -x[1])]

def score_from_texts(user_text: str, original_model_text: str, babbel_text: str) -> Dict:
    confidence = rewrite_confidence(original_model_text, babbel_text)
    flags = get_fact_flags(user_text)
    influence = node_influence_breakdown(user_text)
    heatmap = memory_heatmap()
    inline = {"user": user_text, "original": original_model_text, "rewrite": babbel_text}
    return {
        "rewrite_confidence": round(confidence, 3),
        "fact_flags": flags,
        "influence": influence,
        "memory_heatmap": heatmap,
        "inline": inline,
    }
