#!/bin/bash
set -e

SRC="babbel_core/streamlit_babbel_app.py"
BAK="$SRC.bak.$(date +%s)"
cp "$SRC" "$BAK"

# Remove broken function
sed -i '' '/^def call_openrouter/,/^def build_messages_with_context/d' "$SRC"

# Append a clean replacement
cat >> "$SRC" <<'PY'

def call_openrouter(messages):
    headers = {
        "Authorization": f"Bearer {HARD_CODED_API_KEY}",
        "Content-Type": "application/json",
        "Referer": "http://localhost:8501",
        "Origin": "http://localhost:8501",
        "X-Title": "Babbel Official Dev"
    }

    print("🔥 HEADERS SENT:", headers)

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    print("🔥 PAYLOAD:", payload)

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

echo "✅ Rewritten clean: $SRC"
