#!/bin/bash
set -e

SRC="babbel_core/streamlit_babbel_app.py"
BAK="${SRC}.bak.$(date +%s)"
cp "$SRC" "$BAK"

# remove whole function
sed -E '/^def call_openrouter\(messages\):/,/^def build_messages_with_context\(/d' "$SRC" > "$SRC.tmp"

# append clean version
cat >> "$SRC.tmp" <<'PY'

def call_openrouter(messages):
    headers = {
        "Authorization": f"Bearer {HARD_CODED_API_KEY}",
        "Content-Type": "application/json",
        "Referer": "http://localhost:8501",
        "Origin": "http://localhost:8501",
        "X-Title": "Babbel Official Dev"
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=90)
    if resp.status_code >= 400:
        try:
            detail = resp.json()
        except Exception:
            detail = {"error": resp.text}
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {detail}")
    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError(f"Unexpected API response shape: {data}")
PY

mv "$SRC.tmp" "$SRC"
echo "✅ Overwrote call_openrouter in $SRC"
