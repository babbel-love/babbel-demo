#!/usr/bin/env bash
# Babbel Core — Ultimate Human Experience Upgrade Pack (stdlib-only, idempotent)
# Applies on top of your baseline repo. Safe to re-run.
set -euo pipefail
umask 077

# ---------- detect root package folder ----------
ROOT_DEFAULT="babbel_core"
ROOT="${BABBEL_CORE_ROOT:-$ROOT_DEFAULT}"
if [[ ! -d "$ROOT" && -d "babel_core" ]]; then
  ROOT="babel_core"
fi
mkdir -p "$ROOT"/{core,tests,scripts,adapters}
# ensure packages
: > "$ROOT/__init__.py"
: > "$ROOT/core/__init__.py"
: > "$ROOT/tests/__init__.py"
: > "$ROOT/adapters/__init__.py"

# -----------------------------
# core/config.py (env-driven config)
# -----------------------------
cat > "$ROOT/core/config.py" <<'PY'
from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass
class Config:
    MEMORY_FILE: str
    LOG_JSONL: str
    CONTEXT_ITEMS: int
    MAX_LINES: int
    STYLE_PROFILE: str
    MODEL_NAME: str
    TIMEOUT_S: int

def _int_env(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, str(default)))
    except Exception:
        return default

def load() -> Config:
    return Config(
        MEMORY_FILE=os.environ.get("BABBEL_MEMORY_FILE", "memory_log.json"),
        LOG_JSONL=os.environ.get("BABBEL_LOG_JSONL", "events.jsonl"),
        CONTEXT_ITEMS=_int_env("BABBEL_CONTEXT_ITEMS", 6),
        MAX_LINES=_int_env("BABBEL_MAX_LINES", 6),
        STYLE_PROFILE=os.environ.get("BABBEL_STYLE", "warm_coach"),
        MODEL_NAME=os.environ.get("BABBEL_MODEL", "openrouter/fallback"),
        TIMEOUT_S=_int_env("BABBEL_TIMEOUT_S", 20),
    )
PY

# -----------------------------
# core/observability.py (trace id, utc now, jsonl logger, timers)
# -----------------------------
cat > "$ROOT/core/observability.py" <<'PY'
from __future__ import annotations
import json, uuid, time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

def new_trace_id() -> str:
    return uuid.uuid4().hex

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class jsonl_logger:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
    def write(self, obj: Dict[str, Any]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

@contextmanager
def time_block(_name: str = ""):
    start = time.perf_counter()
    data: Dict[str, Any] = {}
    try:
        yield data
    finally:
        data["elapsed_ms"] = int((time.perf_counter() - start) * 1000)
PY

# -----------------------------
# core/schema.py (extend with optional `ux`)
# -----------------------------
cat > "$ROOT/core/schema.py" <<'PY'
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

# Common emotion aliases normalized for downstream logic.
ALIASES = {
    "rage": "anger",
    "mad": "anger",
    "sadness": "grief",
    "sad": "grief",
    "mourning": "grief",
    "awe": "wonder",
    "surprise": "wonder",
    "guilt": "shame",
    "embarrassment": "shame",
    "anxious": "fear",
    "anxiety": "fear",
}

@dataclass
class FinalPayload:
    trace_id: str
    guiding_line: str
    final_text: str
    emotion: str
    intent: str
    notes: Optional[str]
    tokens_used: Optional[int]
    timestamp_utc: str
    safety: Dict[str, Any]
    ux: Optional[Dict[str, Any]] = None  # NEW: UX block for GUI

def _is_utc_iso(s: str) -> bool:
    try:
        if s.endswith("Z"):
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(s)
        return (dt.tzinfo is not None) and (dt.utcoffset() == timedelta(0))
    except Exception:
        return False

def validate_payload(obj: dict) -> FinalPayload:
    required = ["trace_id", "guiding_line", "final_text", "emotion", "intent", "timestamp_utc", "safety"]
    for k in required:
        if k not in obj:
            raise ValueError(f"missing field: {k}")
    guiding_line = str(obj["guiding_line"]).strip()
    final_text = str(obj["final_text"]).strip()
    if not guiding_line or not final_text:
        raise ValueError("guiding_line and final_text must be non-empty")
    emotion = ALIASES.get(str(obj["emotion"]).lower(), str(obj["emotion"]).lower())
    intent = str(obj["intent"]).lower()
    if not _is_utc_iso(str(obj["timestamp_utc"])):
        raise ValueError("timestamp_utc must be UTC ISO 8601")
    safety = obj["safety"]
    if not (
        isinstance(safety, dict)
        and "blocked" in safety
        and "reasons" in safety
        and isinstance(safety["blocked"], bool)
        and isinstance(safety["reasons"], list)
    ):
        raise ValueError("invalid safety shape")
    ux = obj.get("ux")
    if ux is not None and not isinstance(ux, dict):
        raise ValueError("ux must be a dict or omitted")
    tok = obj.get("tokens_used")
    if tok is not None and not isinstance(tok, int):
        raise ValueError("tokens_used must be int or omitted")
    return FinalPayload(
        trace_id=str(obj["trace_id"]),
        guiding_line=guiding_line,
        final_text=final_text,
        emotion=emotion,
        intent=intent,
        notes=obj.get("notes"),
        tokens_used=tok,
        timestamp_utc=str(obj["timestamp_utc"]),
        safety=safety,
        ux=ux,
    )

def to_dict(fp: FinalPayload) -> dict:
    out = {
        "trace_id": fp.trace_id,
        "guiding_line": fp.guiding_line,
        "final_text": fp.final_text,
        "emotion": fp.emotion,
        "intent": fp.intent,
        "notes": fp.notes,
        "tokens_used": fp.tokens_used,
        "timestamp_utc": fp.timestamp_utc,
        "safety": fp.safety,
    }
    if fp.ux is not None:
        out["ux"] = fp.ux
    return out
PY

# -----------------------------
# core/hx_engine.py (human-experience engine)
# -----------------------------
cat > "$ROOT/core/hx_engine.py" <<'PY'
from __future__ import annotations
import hashlib
from typing import Dict, Any, List

def _seed(*parts: str) -> int:
    h = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return int(h[:8], 16)

def _take(seq: List[Any], n: int) -> List[Any]:
    return seq[: max(0, n)]

def build_extras(user_input: str, emotion: str, intent: str, style_profile: str) -> Dict[str, Any]:
    e = (emotion or "").lower()
    i = (intent or "").lower()
    s = (style_profile or "warm_coach").lower()
    seed = _seed(user_input, e, i, s)

    # Reflection (mirroring)
    if e == "shame":
        reflection = "Quick read: I hear shame and a wish to do right."
    elif e == "anger":
        reflection = "Quick read: I hear anger trying to protect something important."
    elif e == "grief":
        reflection = "Quick read: I hear grief — this really matters."
    elif e == "fear":
        reflection = "Quick read: I hear alarm — your system wants safety."
    elif e == "wonder":
        reflection = "Quick read: I hear curiosity and energy to explore."
    else:
        reflection = "Quick read: I hear you want something practical and kind."

    # Normalization
    if i == "confession":
        norm = "You took a risk by sharing this; that’s courage."
    elif i == "seek guidance":
        norm = "You want a next step, not a lecture."
    elif i == "search for meaning":
        norm = "You’re trying to make sense before you move."
    elif i == "explore":
        norm = "You want low‑risk experiments before committing."
    else:
        norm = "Let’s keep it doable and human‑sized."

    # Options (deterministic rotation)
    choices: List[Dict[str, str]] = []
    if i == "seek guidance":
        choices = [
            {"label": "Tiny step (≤10 min)", "when_it_helps": "Overwhelm or stall.", "first_step": "Set a 10‑minute timer and do the very first move."},
            {"label": "Obstacle‑first", "when_it_helps": "Foggy blockers.", "first_step": "Name the blocker; write one workaround; do only that."},
            {"label": "Two‑option test", "when_it_helps": "Stuck choosing.", "first_step": "List 2 options with 1 tradeoff each; pick one for a 10‑minute test."},
        ]
        if e == "fear":
            choices.insert(0, {"label": "Safety‑first", "when_it_helps": "When alarm is loud.", "first_step": "Thank the alarm; choose one gentle step that adds safety."})
    elif i == "confession":
        choices = [
            {"label": "Name values", "when_it_helps": "Moral fog.", "first_step": "Write the one value you want to stand for here."},
            {"label": "Do one repair", "when_it_helps": "Guilt loops.", "first_step": "Choose a single amends or check‑in you can do today."},
            {"label": "Future guardrail", "when_it_helps": "Prevent repeats.", "first_step": "Add one small friction (reminder/note) before this situation repeats."},
        ]
        if e == "shame":
            choices.append({"label": "Drop self‑attack", "when_it_helps": "Harsh inner talk.", "first_step": "Replace one self‑insult with one specific next action."})
    elif i == "search for meaning":
        choices = [
            {"label": "Value trace", "when_it_helps": "Why bother?", "first_step": "Finish the sentence: “I care about this because…”"},
            {"label": "Carry a lesson", "when_it_helps": "After loss.", "first_step": "Write one lesson you can carry without rushing the pain."},
            {"label": "Tiny experiment", "when_it_helps": "Abstract thinking.", "first_step": "Try a 10‑minute test that expresses that value."},
        ]
        if e == "grief":
            choices.insert(0, {"label": "Make room", "when_it_helps": "Heavy waves.", "first_step": "Give yourself permission to not fix it today."})
    elif i == "explore":
        choices = [
            {"label": "Two reversible tries", "when_it_helps": "Low commitment.", "first_step": "Schedule two low‑cost experiments this week."},
            {"label": "Follow the aliveness", "when_it_helps": "Low motivation.", "first_step": "Spend 15 minutes on what feels alive, then reassess."},
            {"label": "Talk it out", "when_it_helps": "Stuck in head.", "first_step": "Say it aloud once; notice what shifts."},
        ]
        if e == "wonder":
            choices.append({"label": "Keep it playful", "when_it_helps": "Over‑seriousness.", "first_step": "Treat it like a mini‑game; score doesn’t matter yet."})
    else:
        choices = [
            {"label": "One step today", "when_it_helps": "Any stuckness.", "first_step": "Choose the smallest visible step and do it for 10 minutes."},
            {"label": "Ask for perspective", "when_it_helps": "Tunnel vision.", "first_step": "Message one person and ask one focused question."},
            {"label": "Energy check", "when_it_helps": "Low fuel.", "first_step": "Water, breath, 30‑second reset; then choose one step."},
        ]

    # Deterministic rotation
    r = seed % len(choices) if choices else 0
    choices = choices[r:] + choices[:r]

    # Question + CTA
    if i in ("seek guidance", "explore"):
        question = "Which option feels 10‑minute doable right now?"
    elif i == "confession":
        question = "What small repair would honor your values today?"
    elif i == "search for meaning":
        question = "What value is asking to be carried forward?"
    else:
        question = "What’s the smallest next step you’re willing to try?"

    cta = "Pick one option and schedule the first 10 minutes."

    return {
        "reflection": reflection,
        "normalization": norm,
        "choices": choices,
        "question": question,
        "cta": cta,
    }

def compose_brief(extras: Dict[str, Any], max_items: int = 2) -> str:
    lines: List[str] = []
    if extras.get("reflection"):
        lines.append(extras["reflection"])
    if extras.get("normalization"):
        lines.append(extras["normalization"])
    for opt in _take(extras.get("choices", []), max_items):
        lines.append(f"• {opt['label']}: {opt['first_step']}")
    if extras.get("question"):
        lines.append(extras["question"])
    return "\n".join(lines[:6])  # keep human-sized
PY

# -----------------------------
# core/culture_shift.py (toggleable tone adjustments + explanation)
# -----------------------------
cat > "$ROOT/core/culture_shift.py" <<'PY'
from __future__ import annotations
import re
from typing import Tuple

# Very light-touch, opt-in tone adjustments with a short explanation string.
# Goal: reduce friction across communication norms (high-context vs low-context),
# not to stereotype or rewrite content.

def _soften_imperatives(text: str) -> str:
    out_lines = []
    for ln in text.splitlines():
        ln_strip = ln.lstrip()
        # soften "Pick/Choose/Try/Do/Write/Set/List/Give" -> "Consider ..."  (grammar fix)
        out = re.sub(r"^(•\s*)?(Pick|Choose|Try|Do|Write|Set|List|Give)\b", r"\1Consider", ln_strip, flags=re.IGNORECASE)
        # soften "Schedule" -> "You could schedule"
        out = re.sub(r"^(•\s*)?(Schedule)\b", r"\1You could schedule", out, flags=re.IGNORECASE)
        # soften "Ask" -> "You might ask"
        out = re.sub(r"^(•\s*)?(Ask)\b", r"\1You might ask", out, flags=re.IGNORECASE)
        # keep original indentation/bullets
        prefix = ln[: len(ln) - len(ln_strip)]
        out_lines.append(prefix + out)
    return "\n".join(out_lines)

def _sharpen_hedges(text: str) -> str:
    # remove weak hedges "maybe/perhaps/you could/consider" at sentence start
    out = re.sub(r"(?m)^\s*(maybe|perhaps|you could|consider)\s+", "", text, flags=re.IGNORECASE)
    out = re.sub(r"\bkind of\b", "", out, flags=re.IGNORECASE)
    return re.sub(r"\s{2,}", " ", out)

def apply_and_explain(text: str, target: str) -> Tuple[str, str]:
    t = (target or "").strip().lower()
    if not t:
        return text, ""
    if t in {"ja","jp","ja-jp","japanese"}:
        adjusted = _soften_imperatives(text)
        expl = "Tone softened for a higher‑context audience (more permission‑based phrasing, fewer direct imperatives)."
        return adjusted, expl
    if t in {"de","de-de","german"}:
        adjusted = _sharpen_hedges(text)
        expl = "Tone sharpened for a lower‑context audience (clearer directives, fewer hedges)."
        return adjusted, expl
    if t in {"ar","ar-eg","ar-sa","arabic"}:
        adjusted = _soften_imperatives(text)
        expl = "Tone slightly softened and made more invitational."
        return adjusted, expl
    if t in {"zh","zh-cn","zh-tw","cn","chinese"}:
        adjusted = _sharpen_hedges(text)
        expl = "Tone made more direct and pragmatic, minimizing softeners."
        return adjusted, expl
    if t in {"es","es-es","es-mx","spanish"}:
        adjusted = _soften_imperatives(text)
        expl = "Tone softened slightly to reduce direct imperatives."
        return adjusted, expl
    if t in {"fr","fr-fr","french"}:
        adjusted = _soften_imperatives(text)
        expl = "Tone tempered slightly to sound less prescriptive."
        return adjusted, expl
    if t in {"en-us","us","english","en"}:
        return text, "Default directness retained."
    # Unknown target: leave unchanged
    return text, f"No culture profile for “{target}”; left unchanged."
PY

# -----------------------------
# core/rewrite.py (ported + minimal cleanup)
# -----------------------------
cat > "$ROOT/core/rewrite.py" <<'PY'
from __future__ import annotations
import re

def rewrite_response(text: str) -> str:
    t = re.sub(r"\b(I think|perhaps|maybe|it seems)\b", "", text, flags=re.IGNORECASE)
    t = re.sub(r"\b(as an AI|I'm here to help|I hope this helps|I apologize)\b", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip()
PY

# -----------------------------
# core/node_rules.py (guided line + text)
# -----------------------------
cat > "$ROOT/core/node_rules.py" <<'PY'
from __future__ import annotations
from typing import Tuple

def apply_node_rules(text: str, emotion: str, intent: str) -> Tuple[str, str]:
    # guiding_line describes why the shaping happened; we do not alter `text` here.
    if emotion == "shame":
        return text, "You’re holding something unbearable — not because it’s true, but because it feels that way."
    elif emotion == "grief" and intent == "search for meaning":
        return text, "Grief isn’t just pain — it’s proof that something mattered. We’ll stay with that."
    elif emotion == "anger":
        return text, "That edge in your voice? It matters. Let’s hear it without trying to tame it."
    elif emotion == "wonder":
        return text, "There’s something alive in that wondering. Let’s not rush to explain it away."
    elif emotion == "fear" and intent == "seek guidance":
        return text, "I’m with you. We’ll face this carefully — not quickly."
    elif intent == "confession":
        return text, "You’re not asking for advice. You’re asking if it’s still okay to be seen. It is."
    else:
        return text, "Let’s slow this down together and see what’s really here."
PY

# -----------------------------
# core/classifier.py (emotion+intent heuristics)
# -----------------------------
cat > "$ROOT/core/classifier.py" <<'PY'
from __future__ import annotations

def _emo(text: str) -> str:
    t = (text or "").lower()
    if any(w in t for w in ["worthless", "disgust", "ashamed"]): return "shame"
    if any(w in t for w in ["sad", "heartbroken", "loss"]): return "grief"
    if any(w in t for w in ["angry", "rage", "fed up"]): return "anger"
    if any(w in t for w in ["curious", "what if", "open to"]): return "wonder"
    if any(w in t for w in ["scared", "anxious", "afraid", "panic"]): return "fear"
    return "mixed"

def _intent(text: str) -> str:
    t = (text or "").lower()
    if any(w in t for w in ["what should", "need advice", "help me"]): return "seek guidance"
    if any(w in t for w in ["i’m sorry", "i'm sorry", "it’s my fault", "it's my fault", "i feel guilty"]): return "confession"
    if any(w in t for w in ["you never", "why would you", "always do this"]): return "protest"
    if any(w in t for w in ["why", "what does it mean", "what's wrong with me","whats wrong with me"]): return "search for meaning"
    return "explore"

def classify(text: str):
    return {"emotion": _emo(text), "intent": _intent(text)}
PY

# -----------------------------
# core/safety.py (simple input/output gates)
# -----------------------------
cat > "$ROOT/core/safety.py" <<'PY'
from __future__ import annotations
import re
from typing import Tuple, Dict, Any

SELF_HARM_PAT = re.compile(r"\b(kill myself|suicide|end my life)\b", re.IGNORECASE)
PII_PAT = re.compile(r"\b(password|ssn|social security|credit card|cvv)\b", re.IGNORECASE)

def analyze(user_text: str) -> Dict[str, Any]:
    reasons = []
    if SELF_HARM_PAT.search(user_text or ""):
        reasons.append("self_harm")
    if PII_PAT.search(user_text or ""):
        reasons.append("pii")
    return {"blocked": bool(reasons), "reasons": reasons}

def gate(output_text: str) -> Tuple[bool, Dict[str, Any], str]:
    # Minimal output scan; in a real system you'd re-scan and redact if needed.
    blocked = False
    reasons: list[str] = []
    return blocked, {"blocked": blocked, "reasons": reasons}, output_text
PY

# -----------------------------
# core/style_engine.py (brief shaping, max lines)
# -----------------------------
cat > "$ROOT/core/style_engine.py" <<'PY'
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .config import load

@dataclass
class Profile:
    name: str
    max_lines: int

def from_config(cfg=None) -> Profile:
    cfg = cfg or load()
    return Profile(name=str(getattr(cfg, "STYLE_PROFILE", "warm_coach")), max_lines=int(getattr(cfg, "MAX_LINES", 6)))

def apply(text: str, profile: Profile) -> str:
    lines = [ln.rstrip() for ln in (text or "").strip().splitlines() if ln.strip()]
    return "\n".join(lines[: max(1, profile.max_lines)])
PY

# -----------------------------
# core/context.py (recent memory retrieval)
# -----------------------------
cat > "$ROOT/core/context.py" <<'PY'
from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any

def get_recent(n: int, memory_file: str) -> List[Dict[str, Any]]:
    p = Path(memory_file)
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        rows = data[-max(0, int(n)):] 
        out = []
        for r in rows:
            out.append({
                "ts": r.get("ts") or r.get("timestamp"),
                "emotion": r.get("emotion",""),
                "intent": r.get("intent",""),
                "user_input": r.get("user_input") or r.get("input") or "",
                "response": r.get("response") or r.get("final_reply") or "",
            })
        return out
    except Exception:
        return []
PY

# -----------------------------
# core/memory_tracker.py (UTC memory log)
# -----------------------------
cat > "$ROOT/core/memory_tracker.py" <<'PY'
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from .config import load

def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def log_interaction(emotion: str, intent: str, user_input: str, response: str) -> None:
    cfg = load()
    p = Path(cfg.MEMORY_FILE)
    data = []
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            data = []
    data.append({
        "ts": _now_utc_iso(),
        "emotion": emotion,
        "intent": intent,
        "user_input": user_input,
        "response": response
    })
    p.write_text(json.dumps(data[-100:], ensure_ascii=False, indent=2), encoding="utf-8")
PY

# -----------------------------
# core/tokens.py (rough estimate)
# -----------------------------
cat > "$ROOT/core/tokens.py" <<'PY'
from __future__ import annotations

def rough_token_estimate(*texts: str) -> int:
    total = sum(len((t or "")) for t in texts)
    return max(1, total // 4)
PY

# -----------------------------
# core/fallback.py (offline generation path)
# -----------------------------
cat > "$ROOT/core/fallback.py" <<'PY'
from __future__ import annotations
from . import hx_engine

def generate(user_input: str, emotion: str, intent: str, style_profile: str, max_lines: int) -> str:
    ex = hx_engine.build_extras(user_input, emotion, intent, style_profile)
    return hx_engine.compose_brief(ex, max_items=2)
PY

# -----------------------------
# core/orchestrator.py (inject UX + optional culture shift; resilient imports)
# -----------------------------
cat > "$ROOT/core/orchestrator.py" <<'PY'
from __future__ import annotations
import os
from pathlib import Path
from typing import Optional, Dict, Any, List

# Robust adapter import: if OpenRouter missing, use a stub that triggers fallback.
try:
    from ..adapters import openrouter  # type: ignore
except Exception:  # pragma: no cover
    class _OpenRouterStub:
        @staticmethod
        def generate_reply(*_args: Any, **_kwargs: Any) -> str:
            raise NotImplementedError("openrouter adapter not available")
    openrouter = _OpenRouterStub()  # type: ignore

from .observability import new_trace_id, utc_now_iso, jsonl_logger, time_block
from .classifier import classify
from . import safety, rewrite, node_rules, schema, memory_tracker, style_engine, context, tokens, hx_engine, culture_shift
from .config import load

def _craft_prompt(user_input: str, emo: str, intent: str, ctx: List[dict], style_name: str) -> str:
    head = (
        "You are Babbel Core. Respond briefly and concretely.\n"
        f"Style profile: {style_name}\n"
        f"Emotion hint: {emo or '-'} | Intent hint: {intent or '-'}"
    )
    ctx_lines: List[str] = []
    if ctx:
        ctx_lines.append("Recent context:")
        for item in ctx:
            u = (item.get("user_input","") or "").strip().replace("\\n", " ")
            r = (item.get("response","") or "").strip().replace("\\n", " ")
            if u:
                ctx_lines.append(f"- U: {u[:140]}")
            if r:
                ctx_lines.append(f"  A: {r[:140]}")
    body = f"User said:\\n---\\n{user_input}\\n---"
    return "\\n".join(([head] + ctx_lines + [body]))

def _safety_message(reasons: List[str]) -> str:
    if "self_harm" in reasons:
        return (
            "I'm really sorry you're feeling this way. I can't help with that here. "
            "If you might be in immediate danger, please call your local emergency number now. "
            "If you can, consider reaching out to someone you trust or a local crisis hotline."
        )
    if "pii" in reasons:
        return "I can’t help with sharing or handling sensitive credentials. Let’s talk about safer alternatives."
    return "I can’t help with that. We can talk about safety and next steps if you want."

def process_message(user_input: str, user_id: Optional[str] = None) -> Dict[str, Any]:
    cfg = load()
    trace_id = new_trace_id()
    logger = jsonl_logger(Path(cfg.LOG_JSONL))

    # Classification
    with time_block("classify") as tb:
        c = classify(user_input)
    logger.write({"trace_id":trace_id, "step":"classify", "elapsed_ms":tb["elapsed_ms"], "out":c})

    # Early input safety
    with time_block("safety_input") as tb:
        input_scan = safety.analyze(user_input)
    logger.write({"trace_id":trace_id, "step":"safety_input", "elapsed_ms":tb["elapsed_ms"], "out":{k:input_scan[k] for k in ("blocked","reasons")}})
    if input_scan["blocked"]:
        guiding_line = "Decline unsafe request; offer safety-oriented next steps."
        final_text = _safety_message(input_scan["reasons"])
        payload = {
            "trace_id": trace_id,
            "guiding_line": guiding_line,
            "final_text": final_text,
            "emotion": (c["emotion"] or ""),
            "intent": (c["intent"] or ""),
            "notes": "input_safety_triggered",
            "tokens_used": None,
            "timestamp_utc": utc_now_iso(),
            "safety": {"blocked": True, "reasons": input_scan.get("reasons", [])},
            "ux": {
                "reflection": "Safety first.",
                "choices": [],
                "question": "Is there someone you can reach out to right now?",
                "cta": "Please contact local emergency services if you’re in danger.",
                "style_profile": cfg.STYLE_PROFILE,
                "culture_explanation": None,
            },
        }
        fp = schema.validate_payload(payload)
        with time_block("memory_log") as tb:
            memory_tracker.log_interaction(fp.emotion, fp.intent, user_input, fp.final_text)
        logger.write({"trace_id":trace_id, "step":"memory_log", "elapsed_ms":tb["elapsed_ms"]})
        logger.write({"trace_id":trace_id, "step":"return", "payload_keys": list(schema.to_dict(fp).keys())})
        return schema.to_dict(fp)

    # Context retrieval
    with time_block("context") as tb:
        ctx_items = context.get_recent(cfg.CONTEXT_ITEMS, cfg.MEMORY_FILE)
    logger.write({"trace_id":trace_id, "step":"context", "elapsed_ms":tb["elapsed_ms"], "count": len(ctx_items)})

    prompt = _craft_prompt(user_input, c["emotion"], c["intent"], ctx_items, cfg.STYLE_PROFILE)

    # Human-experience extras (precomputed for both fallback and real generations)
    hx_extras = hx_engine.build_extras(user_input, c["emotion"], c["intent"], cfg.STYLE_PROFILE)
    max_ux_items = max(1, min(3, int(os.environ.get("BABBEL_UX_ITEMS", "2"))))

    # Generate (or fallback)
    used_fallback = False
    try:
        with time_block("generate") as tb:
            raw = openrouter.generate_reply(prompt, cfg.MODEL_NAME, cfg.TIMEOUT_S)
        logger.write({"trace_id":trace_id, "step":"generate", "elapsed_ms":tb["elapsed_ms"]})
    except NotImplementedError:
        raw = None
    except Exception as e:  # pragma: no cover
        logger.write({"trace_id":trace_id, "step":"generate_error", "error": repr(e)})
        raw = None

    if raw is None:
        from .fallback import generate as fallback_generate
        with time_block("fallback") as tb:
            raw = fallback_generate(user_input, c["emotion"], c["intent"], cfg.STYLE_PROFILE, cfg.MAX_LINES)
        logger.write({"trace_id":trace_id, "step":"fallback", "elapsed_ms":tb["elapsed_ms"]})
        used_fallback = True

    # Output safety & shaping
    try:
        with time_block("safety_output") as tb:
            blocked, safety_dict, styled = safety.gate(raw)
        logger.write({"trace_id":trace_id, "step":"safety_output", "elapsed_ms":tb["elapsed_ms"], "out":safety_dict})
    except Exception as e:  # pragma: no cover
        logger.write({"trace_id":trace_id, "step":"safety_output_error", "error": repr(e)})
        blocked, safety_dict, styled = False, {"reasons": []}, raw

    if blocked:
        final_text = _safety_message(safety_dict.get("reasons", []))
        guiding_line = "Decline unsafe request; offer safety-oriented next steps."
    else:
        try:
            with time_block("rewrite") as tb:
                cleaned = rewrite.rewrite_response(styled or raw)
            logger.write({"trace_id":trace_id, "step":"rewrite", "elapsed_ms":tb["elapsed_ms"]})
        except Exception as e:  # pragma: no cover
            cleaned = styled or raw
            logger.write({"trace_id":trace_id, "step":"rewrite_error", "error": repr(e)})

        try:
            with time_block("style") as tb:
                profile = style_engine.from_config(cfg)
                shaped = style_engine.apply(cleaned, profile)
            logger.write({"trace_id":trace_id, "step":"style", "elapsed_ms":tb["elapsed_ms"], "profile": profile.name})
        except Exception as e:  # pragma: no cover
            shaped = cleaned
            profile = type("P", (), {"name": "default", "max_lines": 6})()  # lightweight stub
            logger.write({"trace_id":trace_id, "step":"style_error", "error": repr(e)})

        with time_block("node_rules") as tb:
            guided, guiding_line = node_rules.apply_node_rules(shaped, c["emotion"], c["intent"])
        logger.write({"trace_id":trace_id, "step":"node_rules", "elapsed_ms":tb["elapsed_ms"], "line":guiding_line})

        # If we used fallback, prefer the HX brief composition (more human-feeling)
        if used_fallback:
            hx_text = hx_engine.compose_brief(hx_extras, max_items=max_ux_items)
            final_text = hx_text
        else:
            final_text = guided

        # Optional culture shift (after shaping). Re-apply style caps if changed.
        target_culture = os.environ.get("BABBEL_TARGET_CULTURE", "").strip()
        culture_note = None
        if os.environ.get("BABBEL_CULTURE_SHIFT", "").strip() and target_culture:
            with time_block("culture_shift") as tb:
                adjusted, expl = culture_shift.apply_and_explain(final_text, target_culture)
            logger.write({"trace_id":trace_id, "step":"culture_shift", "elapsed_ms":tb["elapsed_ms"], "target": target_culture})
            if adjusted:
                try:
                    final_text = style_engine.apply(adjusted, profile)
                except Exception:
                    final_text = adjusted
            if expl:
                culture_note = expl

    try:
        tokens_used = tokens.rough_token_estimate(user_input, prompt, final_text)
    except Exception:  # pragma: no cover
        tokens_used = None

    ux_block = {
        "reflection": hx_extras.get("reflection"),
        "choices": (hx_extras.get("choices", []) or [])[:max_ux_items],
        "question": hx_extras.get("question"),
        "cta": hx_extras.get("cta"),
        "style_profile": cfg.STYLE_PROFILE,
        "culture_explanation": locals().get("culture_note"),
    }

    payload = {
        "trace_id": trace_id,
        "guiding_line": guiding_line,
        "final_text": final_text,
        "emotion": (c["emotion"] or ""),
        "intent": (c["intent"] or ""),
        "notes": ("fallback_reply" if used_fallback else None),
        "tokens_used": tokens_used,
        "timestamp_utc": utc_now_iso(),
        "safety": {"blocked": bool(blocked), "reasons": safety_dict.get("reasons", [])},
        "ux": ux_block,
    }

    fp = schema.validate_payload(payload)

    with time_block("memory_log") as tb:
        memory_tracker.log_interaction(fp.emotion, fp.intent, user_input, fp.final_text)
    logger.write({"trace_id":trace_id, "step":"memory_log", "elapsed_ms":tb["elapsed_ms"]})
    logger.write({"trace_id":trace_id, "step":"return", "payload_keys": list(schema.to_dict(fp).keys())})

    return schema.to_dict(fp)
PY

# -----------------------------
# tests/test_hx_engine.py
# -----------------------------
cat > "$ROOT/tests/test_hx_engine.py" <<'PY'
import unittest
from babbel_core.core.hx_engine import build_extras, compose_brief

class TestHXEngine(unittest.TestCase):
    def test_build_and_compose(self):
        ex = build_extras("I feel anxious", "fear", "seek guidance", "warm_coach")
        self.assertIn("reflection", ex)
        self.assertGreaterEqual(len(ex.get("choices", [])), 2)
        txt = compose_brief(ex, max_items=2)
        self.assertTrue(len(txt.strip()) > 0)
        self.assertLessEqual(len(txt.splitlines()), 6)

if __name__ == "__main__":
    unittest.main()
PY

# -----------------------------
# tests/test_culture_shift.py
# -----------------------------
cat > "$ROOT/tests/test_culture_shift.py" <<'PY'
import unittest
from babbel_core.core.culture_shift import apply_and_explain, _soften_imperatives

class TestCultureShift(unittest.TestCase):
    def test_soften(self):
        adj, expl = apply_and_explain("Pick one option.\nAsk a friend.", "jp")
        self.assertTrue("softened" in expl.lower() or "invitational" in expl.lower())
        self.assertNotEqual(adj, "")
        # grammar check: no "Consider to"
        softened = _soften_imperatives("Pick one option.")
        self.assertIn("Consider one option.", softened)

    def test_unknown(self):
        adj, expl = apply_and_explain("Do one thing.", "xx")
        self.assertIn("left unchanged", expl.lower())

if __name__ == "__main__":
    unittest.main()
PY

# -----------------------------
# tests/test_schema.py
# -----------------------------
cat > "$ROOT/tests/test_schema.py" <<'PY'
import unittest
from babbel_core.core.schema import validate_payload, to_dict

class TestSchema(unittest.TestCase):
    def test_validate_and_roundtrip(self):
        obj = {
            "trace_id": "t1",
            "guiding_line": "Do the kind thing",
            "final_text": "Okay.",
            "emotion": "sadness",
            "intent": "seek guidance",
            "notes": None,
            "tokens_used": 42,
            "timestamp_utc": "2024-01-01T00:00:00+00:00",
            "safety": {"blocked": False, "reasons": []},
            "ux": {"a": 1},
        }
        fp = validate_payload(obj)
        d = to_dict(fp)
        self.assertEqual(d["emotion"], "grief")
        self.assertIn("ux", d)

    def test_bad_timestamp(self):
        bad = {
            "trace_id":"x","guiding_line":"g","final_text":"f","emotion":"anger",
            "intent":"explore","timestamp_utc":"2020-01-01T00:00:00","safety":{"blocked":False,"reasons":[]}
        }
        with self.assertRaises(ValueError):
            validate_payload(bad)

if __name__ == "__main__":
    unittest.main()
PY

# -----------------------------
# tests/test_orchestrator_ux.py
# -----------------------------
cat > "$ROOT/tests/test_orchestrator_ux.py" <<'PY'
import os, unittest
from babbel_core.core.orchestrator import process_message

class TestOrchestratorUX(unittest.TestCase):
    def test_ux_block_present(self):
        os.environ["BABBEL_CULTURE_SHIFT"] = "1"
        os.environ["BABBEL_TARGET_CULTURE"] = "jp"
        out = process_message("I'm a bit anxious. What should I do?")
        self.assertIn("ux", out)
        self.assertIn("reflection", out["ux"])
        self.assertIsInstance(out["ux"]["choices"], list)
        self.assertIn("style_profile", out["ux"])
        os.environ.pop("BABBEL_CULTURE_SHIFT", None)
        os.environ.pop("BABBEL_TARGET_CULTURE", None)

if __name__ == "__main__":
    unittest.main()
PY

# -----------------------------
# tests/test_orchestrator_fallback.py
# -----------------------------
cat > "$ROOT/tests/test_orchestrator_fallback.py" <<'PY'
import unittest
from babbel_core.core.orchestrator import process_message

class TestOrchestratorFallback(unittest.TestCase):
    def test_fallback_path_runs(self):
        out = process_message("Give me one tiny next step to start writing again.")
        self.assertIsInstance(out, dict)
        self.assertIn("final_text", out)
        self.assertIn("ux", out)

if __name__ == "__main__":
    unittest.main()
PY

# -----------------------------
# scripts/export_history_csv.py (for CSV export)
# -----------------------------
cat > "$ROOT/scripts/export_history_csv.py" <<'PY'
#!/usr/bin/env python3
from __future__ import annotations
import csv, json
from pathlib import Path
from babbel_core.core.config import load

def main():
    cfg = load()
    out_path = Path("memory_export.csv")
    mem = Path(cfg.MEMORY_FILE)
    data = []
    if mem.exists():
        try:
            data = json.loads(mem.read_text(encoding="utf-8"))
        except Exception:
            data = []
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ts","emotion","intent","user_input","response"])
        for row in data:
            w.writerow([row.get("ts",""), row.get("emotion",""), row.get("intent",""), row.get("user_input",""), row.get("response","")])
    print(f"✅ Exported {len(data)} rows -> {out_path}")

if __name__ == "__main__":
    main()
PY
chmod +x "$ROOT/scripts/export_history_csv.py"

# -----------------------------
# scripts/preflight.sh (compile + unit tests + smoke check)
# -----------------------------
cat > "$ROOT/scripts/preflight.sh" <<'PRE'
#!/usr/bin/env bash
set -euo pipefail
ROOT="${BABBEL_CORE_ROOT:-babbel_core}"

echo "🔧 Preflight starting…"
python3 -V

echo "🔎 Byte-compile check…"
python3 -m compileall -q "$ROOT"

echo "🧪 Running unit tests…"
PYTHONPATH="." python3 -m unittest discover -v -s "$ROOT/tests" -t .

echo "🚀 Smoke run (orchestrator)…"
PYTHONPATH="." python3 - "$ROOT" <<'PY'
import os, json
from babbel_core.core.orchestrator import process_message
os.environ["BABBEL_CULTURE_SHIFT"] = "1"
os.environ["BABBEL_TARGET_CULTURE"] = "jp"
out = process_message("Quick test: I'm stressed and need one tiny step.")
print(json.dumps(out, indent=2)[:2000])  # truncate
PY

echo "✅ Preflight complete."
PRE
chmod +x "$ROOT/scripts/preflight.sh"

echo "✅ Ultimate Human Experience upgrade applied to: $ROOT"
echo "Next steps:"
echo "  1) export BABBEL_CORE_ROOT=$ROOT (if needed)"
echo "  2) bash $ROOT/scripts/preflight.sh"
