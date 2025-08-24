import os, json, requests
URL="https://openrouter.ai/api/v1/chat/completions"
key=os.getenv("OPENROUTER_API_KEY","")
headers={
    "Authorization":f"Bearer {key}",
    "Content-Type":"application/json"
}
payload={
    "model":"openrouter/auto",
    "messages":[
        {"role":"system","content":"You are a ping probe."},
        {"role":"user","content":"Reply with Pong."}
    ],
    "temperature":0.0
}
print("ENV KEY PREFIX:", (key[:12] + "********" + key[-4:]) if key else "(missing)")
r=requests.post(URL, headers=headers, json=payload, timeout=60)
print("STATUS", r.status_code)
try:
    print("JSON", json.dumps(r.json(), indent=2)[:800])
except Exception:
    print("TEXT", r.text[:800])
