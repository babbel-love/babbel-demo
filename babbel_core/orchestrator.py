from __future__ import annotations
from .engine import BabbelEngine

def process_message(thread, user_text: str, apply_style: bool = True):
    eng = BabbelEngine(apply_style=apply_style)
    return eng.turn(thread, user_text)
