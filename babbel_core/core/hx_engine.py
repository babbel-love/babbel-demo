from __future__ import annotations
import hashlib
from typing import Dict, Any, List

def _seed(*parts: str) -> int:
    h = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return int(h[:8], 16)

def _take(seq: List[Any], n: int) -> List[Any]:
    return seq[: max(0, n)]

def build_extras(user_input: str, emotion: str, intent: str, style_profile: str) -> Dict[str, Any]:
    e = (emotion or "").lower()
    i = (intent or "").lower()
    s = (style_profile or "warm_coach").lower()
    seed = _seed(user_input, e, i, s)

    # Reflection (mirroring)
    if e == "shame":
        reflection = "Quick read: I hear shame and a wish to do right."
    elif e == "anger":
        reflection = "Quick read: I hear anger trying to protect something important."
    elif e == "grief":
        reflection = "Quick read: I hear grief — this really matters."
    elif e == "fear":
        reflection = "Quick read: I hear alarm — your system wants safety."
    elif e == "wonder":
        reflection = "Quick read: I hear curiosity and energy to explore."
    else:
        reflection = "Quick read: I hear you want something practical and kind."

    # Normalization
    if i == "confession":
        norm = "You took a risk by sharing this; that’s courage."
    elif i == "seek guidance":
        norm = "You want a next step, not a lecture."
    elif i == "search for meaning":
        norm = "You’re trying to make sense before you move."
    elif i == "explore":
        norm = "You want low‑risk experiments before committing."
    else:
        norm = "Let’s keep it doable and human‑sized."

    # Options (deterministic rotation)
    choices: List[Dict[str, str]] = []
    if i == "seek guidance":
        choices = [
            {"label": "Tiny step (≤10 min)", "when_it_helps": "Overwhelm or stall.", "first_step": "Set a 10‑minute timer and do the very first move."},
            {"label": "Obstacle‑first", "when_it_helps": "Foggy blockers.", "first_step": "Name the blocker; write one workaround; do only that."},
            {"label": "Two‑option test", "when_it_helps": "Stuck choosing.", "first_step": "List 2 options with 1 tradeoff each; pick one for a 10‑minute test."},
        ]
        if e == "fear":
            choices.insert(0, {"label": "Safety‑first", "when_it_helps": "When alarm is loud.", "first_step": "Thank the alarm; choose one gentle step that adds safety."})
    elif i == "confession":
        choices = [
            {"label": "Name values", "when_it_helps": "Moral fog.", "first_step": "Write the one value you want to stand for here."},
            {"label": "Do one repair", "when_it_helps": "Guilt loops.", "first_step": "Choose a single amends or check‑in you can do today."},
            {"label": "Future guardrail", "when_it_helps": "Prevent repeats.", "first_step": "Add one small friction (reminder/note) before this situation repeats."},
        ]
        if e == "shame":
            choices.append({"label": "Drop self‑attack", "when_it_helps": "Harsh inner talk.", "first_step": "Replace one self‑insult with one specific next action."})
    elif i == "search for meaning":
        choices = [
            {"label": "Value trace", "when_it_helps": "Why bother?", "first_step": "Finish the sentence: “I care about this because…”"},
            {"label": "Carry a lesson", "when_it_helps": "After loss.", "first_step": "Write one lesson you can carry without rushing the pain."},
            {"label": "Tiny experiment", "when_it_helps": "Abstract thinking.", "first_step": "Try a 10‑minute test that expresses that value."},
        ]
        if e == "grief":
            choices.insert(0, {"label": "Make room", "when_it_helps": "Heavy waves.", "first_step": "Give yourself permission to not fix it today."})
    elif i == "explore":
        choices = [
            {"label": "Two reversible tries", "when_it_helps": "Low commitment.", "first_step": "Schedule two low‑cost experiments this week."},
            {"label": "Follow the aliveness", "when_it_helps": "Low motivation.", "first_step": "Spend 15 minutes on what feels alive, then reassess."},
            {"label": "Talk it out", "when_it_helps": "Stuck in head.", "first_step": "Say it aloud once; notice what shifts."},
        ]
        if e == "wonder":
            choices.append({"label": "Keep it playful", "when_it_helps": "Over‑seriousness.", "first_step": "Treat it like a mini‑game; score doesn’t matter yet."})
    else:
        choices = [
            {"label": "One step today", "when_it_helps": "Any stuckness.", "first_step": "Choose the smallest visible step and do it for 10 minutes."},
            {"label": "Ask for perspective", "when_it_helps": "Tunnel vision.", "first_step": "Message one person and ask one focused question."},
            {"label": "Energy check", "when_it_helps": "Low fuel.", "first_step": "Water, breath, 30‑second reset; then choose one step."},
        ]

    # Deterministic rotation
    r = seed % len(choices) if choices else 0
    choices = choices[r:] + choices[:r]

    # Question + CTA
    if i in ("seek guidance", "explore"):
        question = "Which option feels 10‑minute doable right now?"
    elif i == "confession":
        question = "What small repair would honor your values today?"
    elif i == "search for meaning":
        question = "What value is asking to be carried forward?"
    else:
        question = "What’s the smallest next step you’re willing to try?"

    cta = "Pick one option and schedule the first 10 minutes."

    return {
        "reflection": reflection,
        "normalization": norm,
        "choices": choices,
        "question": question,
        "cta": cta,
    }

def compose_brief(extras: Dict[str, Any], max_items: int = 2) -> str:
    lines: List[str] = []
    if extras.get("reflection"):
        lines.append(extras["reflection"])
    if extras.get("normalization"):
        lines.append(extras["normalization"])
    for opt in _take(extras.get("choices", []), max_items):
        lines.append(f"• {opt['label']}: {opt['first_step']}")
    if extras.get("question"):
        lines.append(extras["question"])
    return "\n".join(lines[:6])  # keep human-sized
