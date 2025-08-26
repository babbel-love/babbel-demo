#!/usr/bin/env bash
set -euo pipefail
KEY="${OPENROUTER_API_KEY:-}"
SITE="${OPENROUTER_SITE_URL:-}"
TITLE="${OPENROUTER_APP_TITLE:-Babbel Local Dev}"
[ -n "$KEY" ] && [ "$KEY" != "sk-or-REPLACE-ME" ] || { echo "ERROR: Set OPENROUTER_API_KEY=sk-or-..."; exit 1; }
echo "GET /models …"
curl -s -o /dev/null -w "HTTP:%{http_code}\n" https://openrouter.ai/api/v1/models -H "Authorization: Bearer $KEY"
cat > /tmp/_or_probe.json <<'JSON'
{"model":"openrouter/auto","messages":[{"role":"user","content":"Reply exactly: Pong."}],"temperature":0}
JSON
echo "POST /chat (server-style)…"
S=$(curl -sS https://openrouter.ai/api/v1/chat/completions -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" --data @/tmp/_or_probe.json -o /tmp/_or_probe_server.json -w "%{http_code}" || echo 000)
echo "HTTP:$S"
if [ "$S" = "200" ]; then exit 0; fi
[ -n "$SITE" ] || { echo "Set OPENROUTER_SITE_URL (e.g., http://localhost:8501)"; exit 2; }
echo "POST /chat (site-style, $SITE)…"
C=$(curl -sS https://openrouter.ai/api/v1/chat/completions -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -H "Referer: $SITE" -H "Origin: $SITE" -H "X-Title: $TITLE" --data @/tmp/_or_probe.json -o /tmp/_or_probe_site.json -w "%{http_code}" || echo 000)
echo "HTTP:$C"
[ "$C" = "200" ] || { echo "401: Update key’s allowed domain to EXACTLY $SITE or use a SERVER key"; exit 3; }
