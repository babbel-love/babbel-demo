from rewrite import rewrite_tone, enforce_babbel_style

def enforce_tone_and_style(text: str) -> str:
    return enforce_babbel_style(rewrite_tone(text))

def summarize_flags(text: str) -> dict:
    t = (text or "").lower()
    hedges = ["maybe","just "," kinda"," kind of"," sort of","probably","perhaps","i think","might ","a bit","little bit"]
    flagged = [h.strip() for h in hedges if h in t]
    return {"hedges_found": flagged, "count": len(flagged)}
