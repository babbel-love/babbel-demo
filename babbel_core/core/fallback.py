from __future__ import annotations
from . import hx_engine

def generate(user_input: str, emotion: str, intent: str, style_profile: str, max_lines: int) -> str:
    ex = hx_engine.build_extras(user_input, emotion, intent, style_profile)
    return hx_engine.compose_brief(ex, max_items=2)
