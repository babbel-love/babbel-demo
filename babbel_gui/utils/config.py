import json, os
CFG_PATH = os.path.expanduser("~/.babbel/config.json")
DEFAULTS = {
    "api_key": "",
    "model_profile": "warm_coach",
    "defaults": {
        "emotion_savvy": False,
        "emit_emotion_series": False,
        "cultural_sensitivity": False,
        "show_metadata": True,
        "live_preview": True,
    }
}
def load():
    try:
        with open(CFG_PATH, "r") as f: return {**DEFAULTS, **json.load(f)}
    except Exception:
        return DEFAULTS.copy()
def save(cfg: dict):
    os.makedirs(os.path.dirname(CFG_PATH), exist_ok=True)
    with open(CFG_PATH, "w") as f: json.dump(cfg, f, indent=2)
    return CFG_PATH
