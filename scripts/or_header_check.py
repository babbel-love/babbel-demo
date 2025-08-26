import os, json, sys, requests
sys.path.insert(0, ".")
from babbel_core import chat  # uses same _resolve_api_key & headers

BASE = "https://openrouter.ai/api/v1"

def mask(tok: str):
    if not tok: return "<empty>"
    return tok[:10] + "…" + tok[-4:]

def show_headers(h):
    redacted = dict(h)
    if "Authorization" in redacted:
        val = redacted["Authorization"]
        if val.startswith("Bearer "):
            redacted["Authorization"] = "Bearer " + mask(val.split(" ",1)[1])
    print("Headers (sanitized):", json.dumps(redacted, indent=2))

def build_headers():
    # Use the same header logic chat.openrouter_request uses
    resp = chat.openrouter_request(payload={"model":"openrouter/auto","messages":[{"role":"user","content":"ping"}],"temperature":0}, x_title="Babbel Probe", api_key=None)
    # We only wanted headers; requests sent already. Rebuild headers explicitly to print:
    api_key = os.getenv("OPENROUTER_API_KEY","")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("OPENROUTER_API_KEY","")
        except Exception:
            pass
    if not api_key:
        raise SystemExit("Missing OPENROUTER_API_KEY")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Title": "Babbel Probe",
    }

def get(path):
    h = build_headers()
    show_headers(h)
    r = requests.get(BASE+path, headers=h, timeout=30)
    print(f"GET {path} -> {r.status_code}")
    if r.status_code >= 400:
        try: print(r.json())
        except Exception: print(r.text[:500])
    return r

def post(path, payload):
    h = build_headers()
    show_headers(h)
    r = requests.post(BASE+path, headers=h, json=payload, timeout=60)
    print(f"POST {path} -> {r.status_code}")
    if r.status_code >= 400:
        try: print(r.json())
        except Exception: print(r.text[:500])
    else:
        try:
            print("Reply:", r.json()["choices"][0]["message"]["content"])
        except Exception:
            print("Raw:", r.text[:240])
    return r

if __name__ == "__main__":
    # 1) /key — singular (OpenRouter uses /key, not /keys)
    get("/key")
    print()
    # 2) /credits
    get("/credits")
    print()
    # 3) /chat/completions
    post("/chat/completions", {"model":"openrouter/auto","messages":[{"role":"user","content":"ping"}],"temperature":0})
