#!/bin/bash
set -e

SRC="babbel_core/streamlit_babbel_app.py"
BAK="${SRC}.bak.$(date +%s)"
cp "$SRC" "$BAK"

awk '
BEGIN { skipping=0 }
/^def call_openrouter\(messages\):/ { skipping=1; print_func(); next }
/^def build_messages_with_context\(/ { skipping=0 }
skipping==0 { print }

function print_func() {
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
' "$SRC" > "$SRC.tmp" && mv "$SRC.tmp" "$SRC"

echo "✅ Patched $SRC cleanly"
