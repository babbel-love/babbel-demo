from __future__ import annotations

def _emo(text: str) -> str:
    t = (text or "").lower()
    if any(w in t for w in ["worthless", "disgust", "ashamed"]): return "shame"
    if any(w in t for w in ["sad", "heartbroken", "loss"]): return "grief"
    if any(w in t for w in ["angry", "rage", "fed up"]): return "anger"
    if any(w in t for w in ["curious", "what if", "open to"]): return "wonder"
    if any(w in t for w in ["scared", "anxious", "afraid", "panic"]): return "fear"
    return "mixed"

def _intent(text: str) -> str:
    t = (text or "").lower()
    if any(w in t for w in ["what should", "need advice", "help me"]): return "seek guidance"
    if any(w in t for w in ["i’m sorry", "i'm sorry", "it’s my fault", "it's my fault", "i feel guilty"]): return "confession"
    if any(w in t for w in ["you never", "why would you", "always do this"]): return "protest"
    if any(w in t for w in ["why", "what does it mean", "what's wrong with me","whats wrong with me"]): return "search for meaning"
    return "explore"

def classify(text: str):
    return {"emotion": _emo(text), "intent": _intent(text)}
