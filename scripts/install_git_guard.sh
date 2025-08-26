#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
HOOK="$ROOT/.git/hooks/pre-commit"
mkdir -p "$ROOT/.git/hooks"
cat > "$HOOK" <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail
echo "[pre-commit] Running Babbel guard tests…"
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi
python - <<'PY'
from babbel_core.anti_chatgpt_guard import guard_output
bad = guard_output("As an AI language model, I cannot browse the internet.")
good = guard_output("Direct, concrete guidance with no boilerplate.")
assert not bad["ok"] and bad["score"] >= 1, "Guard failed to flag boilerplate."
assert good["ok"], "Guard falsely flagged clean text."
print("Guard quick-check OK")
PY
pytest -q babbel_core/tests/test_guard.py
echo "[pre-commit] OK"
HOOK
chmod +x "$HOOK"
echo "Installed pre-commit hook at $HOOK"
