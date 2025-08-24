from . import rewrite, node_rules, review, intent_classifier, emotion_classifier, tone_constants
from .schema import validate_final_output

def run_pipeline(user_input: str) -> dict:
    emotion = emotion_classifier.classify_emotion(user_input)
    intent = intent_classifier.classify_intent(user_input)
    tone = tone_constants.TONE_NEUTRAL
    node = "Embodied Agency"

    guidance = node_rules.apply_node_rules(user_input, emotion, intent)
    rewritten = rewrite.rewrite_tone(user_input)
    styled = rewrite.enforce_babbel_style(rewritten)
    reviewed = review.run_review_stage(styled)
    score = {"rewrite_strength": 0.85, "coherence": 0.92, "emotion_match": 0.88}

    result = {
        "final_text": reviewed["reviewed_text"],
        "metadata": {
            "tone": tone,
            "emotion": emotion,
            "intent": intent,
            "node": node,
            "score": score
        },
        "ux": {
            "reflection": guidance,
            "choices": [
                "Say more about this.",
                "Pause and breathe with me.",
                "Would you like a different kind of reply?"
            ],
            "style_profile": "warm"
        }
    }
    validate_final_output(result)
    return result
