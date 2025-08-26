import os, sys, json, requests

BASE = "https://openrouter.ai/api/v1"
KEY = os.getenv("OPENROUTER_API_KEY", "")

def _hdr():
    return {
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
        "X-Title": "Babbel Healthcheck",
    }

def _mask(k): 
    return (k[:7] + "…" + k[-4:]) if k and len(k) > 10 else "****"

def chk():
    assert KEY, "OPENROUTER_API_KEY missing"
    r = requests.get(BASE + "/key", headers=_hdr(), timeout=30); print("GET /key:", r.status_code); r.raise_for_status()
    r = requests.get(BASE + "/credits", headers=_hdr(), timeout=30); print("GET /credits:", r.status_code); r.raise_for_status()
    payload = {"model": os.getenv("OPENROUTER_MODEL","openrouter/auto"),
               "messages":[{"role":"system","content":"Say: Pong. How can I help?"},{"role":"user","content":"ping"}]}
    r = requests.post(BASE + "/chat/completions", headers=_hdr(), json=payload, timeout=45)
    print("POST /chat:", r.status_code); r.raise_for_status()
    print("OK (key:", _mask(KEY), ")")

if __name__ == "__main__":
    chk()
