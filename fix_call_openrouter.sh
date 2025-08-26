#!/bin/bash
set -e

SRC="babbel_core/streamlit_babbel_app.py"
BAK="babbel_core/streamlit_babbel_app.py.bak.$(date +%s)"

cp "$SRC" "$BAK"

awk '
BEGIN { inside=0 }
/^def call_openrouter\(messages\):/ { inside=1; print "def call_openrouter(messages) {"; next }
/^def build_messages_with_context\(/ { inside=0 }
inside == 1 { next }
{ print }
/^def build_messages_with_context\(/ {
  print ""
  print "def call_openrouter(messages):"
  print "    headers = {"
  print "        \"Authorization\": f\"Bearer {HARD_CODED_API_KEY}\","
  print "        \"Content-Type\": \"application/json\","
  print "        \"Referer\": \"http://localhost:8501\","
  print "        \"Origin\": \"http://localhost:8501\","
  print "        \"X-Title\": \"Babbel Official Dev\""
  print "    }"
  print ""
  print "    payload = {"
  print "        \"model\": model,"
  print "        \"messages\": messages,"
  print "        \"temperature\": temperature,"
  print "    }"
  print ""
  print "    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=90)"
  print "    if resp.status_code >= 400:"
  print "        try:"
  print "            detail = resp.json()"
  print "        except Exception:"
  print "            detail = {\"error\": resp.text}"
  print "        raise RuntimeError(f\"OpenRouter error {resp.status_code}: {detail}\")"
  print "    data = resp.json()"
  print "    try:"
  print "        return data[\"choices\"][0][\"message\"][\"content\"]"
  print "    except Exception:"
  print "        raise RuntimeError(f\"Unexpected API response shape: {data}\")"
  print ""
}
' "$BAK" > "$SRC"

echo "✅ Patched: $SRC"
