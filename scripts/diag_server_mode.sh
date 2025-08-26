#!/usr/bin/env bash
set -euo pipefail
cd "${BABEL_ROOT:-$PWD}"
: "${OPENROUTER_API_KEY:?Set OPENROUTER_API_KEY or write it to ~/.streamlit/secrets.toml}"
python - <<'PY'
import os, json, requests
key = os.getenv("OPENROUTER_API_KEY","")
masked = key[:7] + "…" + key[-4:] if len(key)>=12 else "(short)"
print("Auth (masked):", masked)
h={"Authorization":f"Bearer {key}","Content-Type":"application/json","X-Title":"Babbel Diag"}
r=requests.get("https://openrouter.ai/api/v1/key", headers=h, timeout=30)
print("GET /key:", r.status_code)
b={"model":os.getenv("OPENROUTER_MODEL","openrouter/auto"),"messages":[{"role":"user","content":"ping"}]}
r=requests.post("https://openrouter.ai/api/v1/chat/completions", headers=h, json=b, timeout=60)
print("POST /chat:", r.status_code)
if r.ok:
    print("Reply:", r.json()["choices"][0]["message"]["content"])
PY
