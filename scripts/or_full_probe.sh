#!/usr/bin/env bash
set -euo pipefail
: "${OPENROUTER_API_KEY:?Set OPENROUTER_API_KEY in env or secrets}"

base="https://openrouter.ai/api/v1"
auth="Authorization: Bearer ${OPENROUTER_API_KEY}"

echo "== GET /key"
curl -sS -D - -o /dev/null -H "${auth}" "${base}/key" | sed -n '1,12p'

echo
echo "== GET /credits"
curl -sS -D - -o /dev/null -H "${auth}" "${base}/credits" | sed -n '1,12p'

echo
echo "== POST /chat (Authorization only)"
payload='{"model":"openrouter/auto","messages":[{"role":"user","content":"ping"}],"temperature":0}'
curl -sS -D - \
  -H "${auth}" \
  -H "Content-Type: application/json" \
  -H "X-Title: Babbel Probe" \
  -X POST "${base}/chat/completions" \
  --data "${payload}" \
  -o >(jq -r '.choices[0].message.content' 2>/dev/null || cat >/dev/null) \
| sed -n '1,12p'
echo
