from __future__ import annotations
from .rewrite import enforce_babbel_style

def apply_protocols(text: str, enabled: bool = True) -> str:
    return enforce_babbel_style(text) if enabled else text
