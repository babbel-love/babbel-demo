from rewrite import rewrite_tone, enforce_babbel_style

def run_review_stage(draft: str) -> dict:
    styled = enforce_babbel_style(rewrite_tone(draft or ""))
    return {
        "reviewed_text": styled,
        "quick_check": "Tone strengthened. Style rewritten to match Babbel voice."
    }
