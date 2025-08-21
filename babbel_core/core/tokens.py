from __future__ import annotations

def rough_token_estimate(*texts: str) -> int:
    total = sum(len((t or "")) for t in texts)
    return max(1, total // 4)
