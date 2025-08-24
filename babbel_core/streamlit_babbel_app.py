# babbel_core/streamlit_babbel_app.py
import os, json, csv, requests, math
from datetime import datetime
from pathlib import Path
import streamlit as st

# --- Optional local style helpers ---
try:
    from rewrite import rewrite_tone, enforce_babbel_style
    def babbelize(txt: str) -> str:
        try:
            return enforce_babbel_style(rewrite_tone(txt)).strip()
        except Exception:
            return txt
except Exception:
    def babbelize(txt: str) -> str:
        return txt

# --- Local classifiers & node guidance ---
try:
    from intent_classifier import classify_intent
except Exception:
    def classify_intent(_): return "explore"

try:
    from emotion_classifier import classify_emotion
except Exception:
    def classify_emotion(_): return "mixed"

try:
    from node_rules import apply_node_rules
except Exception:
    def apply_node_rules(_t,_e,_i): return ""

# --- Optional speech protocols ---
def _load_json_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

SPEECH = _load_json_file(str(Path(__file__).with_name("speech_protocols.json")))

def quick_protocol(msg: str):
    t = msg.lower().strip()
    if any(x in t for x in ("hi", "hello", "hey")) and "greeting" in SPEECH:
        return SPEECH["greeting"]
    if "help" in t and "help" in SPEECH:
        return SPEECH["help"]
    if "thanks" in t and "thank" in t and "thanks" in SPEECH:
        return SPEECH["thanks"]
    if any(x in t for x in ("bye", "goodbye", "later")) and "farewell" in SPEECH:
        return SPEECH["farewell"]
    return None

# --- Config & constants ---
st.set_page_config(page_title="Babbel Core — Streamlit (OpenRouter)", page_icon="🧠", layout="centered")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
HARD_CODED_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
SYSTEM_PROMPT = (
    "You are Babbel. Respond concisely, concretely, and without filler. "
    "Be direct, specific, and pragmatic. Avoid hedges like 'maybe'/'just'. "
    "When helpful, provide short steps or a crisp summary. "
    "If the user asks for recent facts, be explicit about uncertainty."
)

SESSIONS_DIR = Path("sessions"); SESSIONS_DIR.mkdir(exist_ok=True)

EMOTION_SCORE = {
    "shame": -2.0, "grief": -1.5, "anger": -1.0, "fear": -0.5,
    "mixed": 0.0, "curious": 0.25, "wonder": 0.5, "relief": 1.0, "calm": 1.25
}

def emotion_to_value(label: str) -> float:
    return EMOTION_SCORE.get(label, 0.0)

def friendly_title_from_first_user(messages):
    for m in messages:
        if m.get("role") == "user":
            words = str(m.get("content","")).strip().split()
            return (" ".join(words[:8]) or "Untitled").strip().rstrip(".")[:60]
    return "Untitled"

def build_messages_with_context(history, n_pairs: int):
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    tail = history[-(n_pairs*2):] if n_pairs > 0 else history
    for m in tail:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role not in ("user","assistant","system"):
            role = "user"
        msgs.append({"role": role, "content": str(content)[:4000]})
    return msgs

def call_openrouter(model: str, temperature: float, messages):
    headers = {
        "Authorization": f"Bearer {HARD_CODED_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "Babbel Core (Streamlit)",
        "HTTP-Referer": "http://localhost:8501/",
    }
    payload = {"model": model, "messages": messages, "temperature": temperature}
    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=90)
    except requests.exceptions.Timeout as e:
        raise RuntimeError("OpenRouter error 408: Request timeout. Try again.") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error: {e}") from e

    if resp.status_code >= 400:
        body = resp.text or ""
        try:
            body = json.dumps(resp.json())
        except Exception:
            pass
        snippet = (body[:300] + ("…" if len(body) > 300 else ""))
        hint = ""
        if resp.status_code in (408,429) or 500 <= resp.status_code < 600:
            hint = " Hint: retry in a few seconds."
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {snippet}{hint}")
    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError(f"Unexpected API response shape: {data}")

def cultural_shift_explanation(user_text: str, assistant_text: str, style_applied: bool) -> str:
    u = user_text.lower(); a = assistant_text.lower()
    softened = any(w in u for w in ["maybe","just","kinda","sort of"])
    direct = any(w in a for w in ["do this","use","must","next"])
    if style_applied and softened and direct:
        return "Tightened hedged phrasing and delivered a more direct, low-context answer."
    if style_applied and not softened:
        return "Kept your direct tone; removed filler to match Babbel style."
    if not style_applied and softened:
        return "Maintained your softer tone without enforcing directness."
    return "No notable cultural shift detected."

def ensure_state():
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("meta_rows", [])   # one per assistant turn
    st.session_state.setdefault("emotion_series", [])  # numeric sparkline

ensure_state()

# --- Title & Caption ---
st.title("🧠 Babbel Core — Streamlit + OpenRouter")
st.caption("Production-tuned chat with metadata, cultural shift notes, session persistence, and a mini emotion sparkline.")

# === Sidebar ===
st.sidebar.header("Model & Memory")
model = st.sidebar.text_input("Model ID", value="openrouter/auto")
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.3, 0.1)
context_turns = st.sidebar.slider("Context turns (last N exchanges)", 1, 30, 10, 1)
use_babbel_style = st.sidebar.checkbox("Apply Babbel style", value=True)
use_culture_shift = st.sidebar.checkbox("Cultural Shift Compensation", value=True)
show_context_preview = st.sidebar.checkbox("Show context preview", value=False)

# Ping
if st.sidebar.button("Ping OpenRouter"):
    try:
        _ = call_openrouter(model, 0.0, [
            {"role":"system","content":"You are a minimal responder."},
            {"role":"user","content":"Say Pong."}
        ])
        st.sidebar.success("Pong.")
    except Exception as e:
        st.sidebar.error(str(e))

# Sessions
st.sidebar.markdown("---")
st.sidebar.subheader("Sessions")
search = st.sidebar.text_input("Search sessions", "")
def _list_sessions():
    items = []
    for p in sorted(SESSIONS_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            title = data.get("thread_name") or p.stem
        except Exception:
            title = p.stem
        if not search or search.lower() in title.lower():
            items.append((title, p.name))
    return items

sess_items = _list_sessions()
sel_label = st.sidebar.selectbox("Choose", [f"{t}  ·  {f}" for t,f in sess_items] or ["(no sessions)"])

c1,c2,c3,c4,c5 = st.sidebar.columns(5)
with c1:
    if st.button("New"):
        st.session_state["messages"] = []
        st.session_state["meta_rows"] = []
        st.session_state["emotion_series"] = []
        st.rerun()
with c2:
    if st.button("Save"):
        title = friendly_title_from_first_user(st.session_state["messages"])
        payload = {
            "thread_name": title,
            "model": model,
            "temperature": float(temperature),
            "memory_messages_number": int(context_turns),
            "messages": st.session_state["messages"],
            "meta_rows": st.session_state["meta_rows"],
            "emotion_series": st.session_state["emotion_series"],
            "saved_at": datetime.utcnow().isoformat()+"Z",
        }
        sid = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        path = SESSIONS_DIR / f"{sid}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        st.sidebar.success(f"Saved: {path.name}")
with c3:
    if st.button("Load"):
        if sess_items:
            fname = sess_items[[f"{t}  ·  {f}" for t,f in sess_items].index(sel_label)][1]
            data = json.loads((SESSIONS_DIR/fname).read_text(encoding="utf-8"))
            st.session_state["messages"] = data.get("messages", [])
            st.session_state["meta_rows"] = data.get("meta_rows", [])
            st.session_state["emotion_series"] = data.get("emotion_series", [])
            st.sidebar.success(f"Loaded {fname}")
            st.rerun()
with c4:
    if st.button("Delete"):
        if sess_items:
            fname = sess_items[[f"{t}  ·  {f}" for t,f in sess_items].index(sel_label)][1]
            try:
                (SESSIONS_DIR/fname).unlink(missing_ok=True)
                st.sidebar.success(f"Deleted {fname}")
                st.rerun()
            except Exception as e:
                st.sidebar.error(str(e))
with c5:
    if st.button("Duplicate"):
        if sess_items:
            fname = sess_items[[f"{t}  ·  {f}" for t,f in sess_items].index(sel_label)][1]
            src = SESSIONS_DIR/fname
            dst = SESSIONS_DIR/(src.stem + "-copy.json")
            try:
                dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
                st.sidebar.success(f"Duplicated to {dst.name}")
                st.rerun()
            except Exception as e:
                st.sidebar.error(str(e))

# Export
def export_csv(path: Path, messages, meta_rows):
    headers = ["role","content","intent","emotion","node_guidance","style_applied","cultural_shift_explanation","timestamp"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        a_meta_iter = iter(meta_rows)
        for m in messages:
            intent = m.get("intent","")
            emotion = m.get("emotion","")
            node = ""
            styled = ""
            shift = ""
            ts = m.get("ts","")
            if m.get("role") == "assistant":
                meta = next(a_meta_iter, {})
                node = meta.get("node_guidance","")
                styled = str(meta.get("style_applied", False))
                shift = meta.get("cultural_shift_explanation","")
            w.writerow([m.get("role",""), m.get("content",""), intent, emotion, node, styled, shift, ts])

st.sidebar.markdown("---")
csa, csb = st.sidebar.columns(2)
with csa:
    if st.button("Export JSON"):
        title = friendly_title_from_first_user(st.session_state["messages"])
        payload = {
            "thread_name": title,
            "model": model,
            "temperature": float(temperature),
            "memory_messages_number": int(context_turns),
            "messages": st.session_state["messages"],
            "meta_rows": st.session_state["meta_rows"],
            "emotion_series": st.session_state["emotion_series"],
            "exported_at": datetime.utcnow().isoformat()+"Z",
        }
        sid = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        path = SESSIONS_DIR / f"{sid}-export.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        st.sidebar.success(f"JSON exported: {path.name}")
with csb:
    if st.button("Export CSV"):
        sid = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        path = SESSIONS_DIR / f"{sid}-export.csv"
        export_csv(path, st.session_state["messages"], st.session_state["meta_rows"])
        st.sidebar.success(f"CSV exported: {path.name}")

# Emotion sparkline (last 20)
st.sidebar.header("Emotion sparkline")
try:
    data = st.session_state["emotion_series"][-20:]
    st.sidebar.line_chart(data)
except Exception:
    st.sidebar.write("No data yet.")

# === Chat history render ===
for msg in st.session_state.messages:
    with st.chat_message(msg.get("role","user")):
        st.markdown(msg.get("content",""))
        if msg.get("role") == "assistant" and msg.get("meta"):
            meta = msg["meta"]
            with st.expander("Metadata"):
                st.write(
                    f"Intent: **{meta.get('intent','')}** · "
                    f"Emotion: **{meta.get('emotion','')}** · "
                    f"Node/Guidance: **{meta.get('node_guidance','')}** · "
                    f"Style applied: **{meta.get('style_applied', False)}**"
                )
                if meta.get("cultural_shift_explanation"):
                    st.caption(f"Explanation: {meta['cultural_shift_explanation']}")

# === Input & turn ===
st.markdown("---")
st.caption("Tip: Press Enter to send. Use Shift+Enter for a newline.")
prompt = st.chat_input("Type your message…")

if prompt:
    now = datetime.utcnow().isoformat()+"Z"
    user_intent = classify_intent(prompt)
    user_emotion = classify_emotion(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "intent": user_intent, "emotion": user_emotion, "ts": now})
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"Intent: {user_intent} · Emotion: {user_emotion}")

    quick = quick_protocol(prompt)
    if quick is not None:
        assistant_raw = quick
    else:
        messages_for_api = build_messages_with_context(st.session_state.messages, context_turns)
        if show_context_preview:
            st.expander("Context preview").json(messages_for_api)
        try:
            assistant_raw = call_openrouter(model, temperature, messages_for_api)
        except Exception as e:
            assistant_raw = f"⚠️ Error: {e}"

    styled_text = babbelize(assistant_raw) if use_babbel_style else assistant_raw
    a_intent = classify_intent(styled_text)
    a_emotion = classify_emotion(styled_text)
    guidance = apply_node_rules(styled_text, a_emotion, a_intent) or ""

    shift_exp = cultural_shift_explanation(prompt, styled_text, bool(use_babbel_style)) if use_culture_shift else ""

    meta = {
        "intent": a_intent,
        "emotion": a_emotion,
        "node_guidance": guidance,
        "style_applied": bool(use_babbel_style),
        "cultural_shift_explanation": shift_exp,
    }

    st.session_state["meta_rows"].append(meta)
    st.session_state["emotion_series"].append(emotion_to_value(a_emotion))

    st.session_state.messages.append({"role": "assistant", "content": styled_text, "meta": meta, "ts": now})
    with st.chat_message("assistant"):
        st.markdown(styled_text)
        with st.expander("Metadata"):
            st.write(
                f"Intent: **{a_intent}** · "
                f"Emotion: **{a_emotion}** · "
                f"Node/Guidance: **{guidance}** · "
                f"Style applied: **{bool(use_babbel_style)}**"
            )
            if shift_exp:
                st.caption(f"Explanation: {shift_exp}")

# Footer (quiet)
st.markdown(" ")
