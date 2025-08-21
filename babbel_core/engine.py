from babbel.core.session_state import SessionState
from babbel.engine.prompt_builder import build_messages
import os, requests, traceback
from typing import Dict

class BabbelEngine:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        print("[BabbelEngine] Initialized. Key set:", bool(self.api_key))

    def reply(self, user_text: str) -> Dict:
        print("[BabbelEngine] User text:", repr(user_text))
        if not self.api_key:
            print("[BabbelEngine] No OPENROUTER_API_KEY detected")
            return {"text": "[No API key set]", "emotions": {"neutral": 1.0}, "meta": {}}
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {"model":"openai/gpt-4o-mini","messages":[{"role":"user","content":user_text}]}
            print("[BabbelEngine] POST", url)
            r = 
# === Babbel: enforce protocol system prompt ===
try:
    snap = SessionState.instance().snapshot()
    if 'payload' in locals() and isinstance(payload, dict) and 'messages' in payload:
        payload['messages'] = build_messages(payload['messages'], snap.show_metadata)
    elif 'data' in locals() and isinstance(data, dict) and 'messages' in data:
        data['messages'] = build_messages(data['messages'], snap.show_metadata)
except Exception:
    pass

# === Babbel: enforce protocol system prompt (always-on) ===
snap = SessionState.instance().snapshot()
if 'payload' in locals() and isinstance(payload, dict) and 'messages' in payload:
    payload['messages'] = build_messages(payload['messages'], snap.show_metadata)
elif 'data' in locals() and isinstance(data, dict) and 'messages' in data:
    data['messages'] = build_messages(data['messages'], snap.show_metadata)
requests.post(url, headers=headers, json=payload, timeout=60)
            print("[BabbelEngine] Status:", r.status_code)
            if r.status_code != 200:
                print("[BabbelEngine] Body:", r.text[:500])
                return {"text": f"[Model error {r.status_code}]", "emotions": {"frustrated": 1.0}, "meta": {"raw": r.text[:500]}}
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            print("[BabbelEngine] OK. Length:", len(text))
            return {"text": text, "emotions": {"neutral": 1.0}, "meta": {"usage": data.get("usage", {})}}
        except Exception as e:
            print("[BabbelEngine] Exception:", e)
            traceback.print_exc()
            return {"text": f"[Exception: {e}]", "emotions": {"frustrated": 1.0}, "meta": {}}
