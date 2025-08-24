import os, json, csv, glob, uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

import requests
import streamlit as st

APP_TITLE = "🧠 Babbel Core — Streamlit + OpenRouter"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
SESSIONS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sessions"))
os.makedirs(SESSIONS_DIR, exist_ok=True)

SYSTEM_PROMPT = (
    "You are Babbel. Respond concisely, concretely, and without filler. "
    "Be direct, specific, and pragmatic. Avoid hedges like 'maybe' or 'just'. "
    "If the user asks for recent facts, be explicit about uncertainty."
)

def _env(n: str, d: str = "") -> str: return os.getenv(n, d)
def _env_key() -> str: return _env("OPENROUTER_API_KEY")
def _env_site() -> str: return _env("OPENROUTER_SITE_URL", "http://localhost:8501").rstrip("/")
def _env_title() -> str: return _env("OPENROUTER_APP_TITLE", "Babbel Local Dev")

# ---- Optional imports with fallbacks ----
try:
    from rewrite import rewrite_tone, enforce_babbel_style  # type: ignore
    def babbelize(txt: str) -> str:
        try: return enforce_babbel_style(rewrite_tone(txt)).strip()
        except Exception: return txt
except Exception:
    def babbelize(txt: str) -> str: return txt

try:
    from intent_classifier import classify_intent  # type: ignore
except Exception:
    def classify_intent(text: str) -> str: return "explore"

try:
    from emotion_classifier import classify_emotion  # type: ignore
except Exception:
    def classify_emotion(text: str) -> str: return "mixed"

try:
    from node_rules import apply_node_rules  # type: ignore
except Exception:
    def apply_node_rules(text, emotion, intent): return "Let’s slow this down together and see what’s really here."

try:
    from memory_tracker import log_interaction, get_recent_emotions  # type: ignore
except Exception:
    def log_interaction(*args, **kwargs): pass
    def get_recent_emotions(n=10): return []

try:
    from thread import ConversationThread  # type: ignore
except Exception:
    class ConversationThread:
        def __init__(self, thread_name, model, temperature, memory_messages_number):
            self.thread_name = thread_name
            self.model = model
            self.temperature = float(temperature)
            self.memory_messages_number = int(memory_messages_number)
            self.messages = []
            self.thread_id = uuid.uuid4().hex
        def to_dict(self): return self.__dict__
        @classmethod
        def from_dict(cls, data):
            obj = cls(
                data.get("thread_name","Untitled"),
                data.get("model","openrouter/auto"),
                data.get("temperature",0.0),
                data.get("memory_messages_number",10),
            )
            obj.messages = data.get("messages",[])
            obj.thread_id = data.get("thread_id") or obj.thread_id
            return obj
        def save(self, directory):
            os.makedirs(directory, exist_ok=True)
            with open(os.path.join(directory, f"{self.thread_id}.json"), "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        @classmethod
        def load(cls, path):
            with open(path, "r", encoding="utf-8") as f:
                return cls.from_dict(json.load(f))

def _key_status_badge():
    key = _env_key()
    if key.startswith("sk-or-") and len(key) > 20: st.sidebar.success("API key detected in env.")
    else: st.sidebar.error("No API key in env. Start app with OPENROUTER_API_KEY set.")

def _build_messages(history: List[Dict[str, Any]], n_pairs: int) -> List[Dict[str, Any]]:
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    tail = history[-(n_pairs*2):] if n_pairs > 0 else history
    for m in tail:
        role = m.get("role", "user")
        content = str(m.get("content", ""))[:4000]
        if role not in ("user", "assistant", "system"): role = "user"
        msgs.append({"role": role, "content": content})
    return msgs

def _call_openrouter(model: str, temperature: float, messages: List[Dict[str, Any]]) -> str:
    key = _env_key()
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Referer": _env_site(),
        "Origin": _env_site(),
        "X-Title": _env_title(),
    }
    payload = {"model": model, "messages": messages, "temperature": float(temperature)}
    r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=90)
    if r.status_code >= 400:
        try: detail = r.json()
        except Exception: detail = {"error": r.text}
        raise RuntimeError(f"OpenRouter error {r.status_code}: {json.dumps(detail)[:300]}")
    data = r.json()
    try: return data["choices"][0]["message"]["content"]
    except Exception: raise RuntimeError(f"Unexpected API response shape: {json.dumps(data)[:300]}")

def _cultural_shift_explanation(user_text: str, assistant_text: str, style_applied: bool) -> str:
    if not style_applied: return "Cultural Shift Compensation is off."
    u = user_text.lower(); a = assistant_text.lower()
    if any(w in u for w in ("maybe","just","kinda","sort of")) and not any(w in a for w in ("maybe","just","kinda","sort of")):
        return "Softened/hedged phrasing was normalized to direct language to avoid misinterpretation across cultures."
    return "No cultural shifts detected beyond tone normalization."

def _emotion_to_value(label: str) -> int:
    return {"shame":-2,"grief":-1,"fear":-1,"anger":0,"mixed":0,"wonder":1}.get(label,0)

def _session_files() -> List[str]: return sorted(glob.glob(os.path.join(SESSIONS_DIR, "*.json")))
def _load_session(path: str) -> "ConversationThread": return ConversationThread.load(path)
def _save_session(ct: "ConversationThread"): ct.save(SESSIONS_DIR)

def _export_csv(ct: "ConversationThread", path_csv: str):
    rows=[]
    for m in ct.messages:
        md=m.get("metadata",{})
        rows.append({
            "timestamp":m.get("timestamp",""),
            "role":m.get("role",""),
            "content":m.get("content",""),
            "intent":md.get("intent",""),
            "emotion":md.get("emotion",""),
            "node_guidance":md.get("node_guidance",""),
            "style_applied":md.get("style_applied",False),
            "cultural_shift_explanation":md.get("cultural_shift_explanation",""),
        })
    with open(path_csv,"w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()) if rows else [
            "timestamp","role","content","intent","emotion","node_guidance","style_applied","cultural_shift_explanation"
        ])
        writer.writeheader()
        for r in rows: writer.writerow(r)

st.set_page_config(page_title="Babbel Core — Streamlit (OpenRouter)", page_icon="🧠", layout="centered")
st.title(APP_TITLE)
st.caption("OpenRouter-backed chat with Babbel style, cultural shift notes, session persistence, and an emotion sparkline.")

st.sidebar.header("Model & Memory")
model = st.sidebar.text_input("Model ID", value="openrouter/auto")
temperature = st.sidebar.slider("Temperature",0.0,1.5,0.3,0.1)
context_turns = st.sidebar.slider("Context turns (last N exchanges)",1,30,10,1)
use_babbel_style = st.sidebar.checkbox("Apply Babbel style",True)
apply_cultural_shift = st.sidebar.checkbox("Cultural Shift Compensation",True)
show_context_preview = st.sidebar.checkbox("Show context preview",False)

st.sidebar.markdown("---"); _key_status_badge()

def _ping():
    try:
        _ = _call_openrouter(model,0.0,[{"role":"system","content":"You are a ping probe."},{"role":"user","content":"Reply Pong."}])
        st.sidebar.success("Pong.")
    except Exception as e:
        st.sidebar.error(str(e))
if st.sidebar.button("Ping OpenRouter"): _ping()

st.sidebar.markdown("---"); st.sidebar.subheader("Sessions")
if "thread" not in st.session_state:
    st.session_state.thread = ConversationThread("Untitled", model, temperature, context_turns)

def _refresh_session_list(): st.session_state.available_sessions = _session_files()
if "available_sessions" not in st.session_state: _refresh_session_list()

colA,colB,colC,colD = st.sidebar.columns([1,1,1,1],vertical_alignment="center")
with colA:
    if st.button("New"):
        st.session_state.thread = ConversationThread("Untitled", model, temperature, context_turns)
        st.session_state.messages=[]
with colB:
    if st.button("Save"): _save_session(st.session_state.thread); _refresh_session_list()
with colC:
    if st.button("Duplicate"):
        t=st.session_state.thread
        clone=ConversationThread((t.thread_name or "Untitled")+" (copy)",t.model,t.temperature,t.memory_messages_number)
        clone.messages=list(t.messages); _save_session(clone); _refresh_session_list()
with colD:
    if st.button("Delete"):
        for p in _session_files():
            try:
                with open(p,"r",encoding="utf-8") as f:
                    if json.load(f).get("thread_id")==st.session_state.thread.thread_id:
                        os.remove(p); _refresh_session_list(); st.success("Deleted session."); break
            except Exception: pass

selected_path = st.sidebar.selectbox("Load session",["(choose)"]+st.session_state.available_sessions)
if selected_path != "(choose)":
    try:
        st.session_state.thread=_load_session(selected_path)
        st.session_state.messages=st.session_state.thread.messages.copy()
        st.sidebar.success("Loaded.")
    except Exception as e:
        st.sidebar.error(f"Load failed: {e}")

st.sidebar.subheader("Export")
if st.sidebar.button("Export CSV"):
    out_csv=os.path.join(SESSIONS_DIR,f"{st.session_state.thread.thread_id}.csv")
    try: _export_csv(st.session_state.thread,out_csv); st.sidebar.success(f"CSV saved: {out_csv}")
    except Exception as e: st.sidebar.error(f"CSV error: {e}")
if st.sidebar.button("Export JSON"):
    try: _save_session(st.session_state.thread); st.sidebar.success("JSON saved.")
    except Exception as e: st.sidebar.error(f"JSON error: {e}")

st.sidebar.header("🧭 Emotion Sparkline")
def _spark_values():
    vals=[]
    for m in st.session_state.thread.messages[-40:]:
        if m.get("role")=="assistant":
            emo=m.get("metadata",{}).get("emotion","mixed"); vals.append(_emotion_to_value(emo))
    return vals[-20:] or [0]
try: st.sidebar.line_chart(_spark_values())
except Exception: st.sidebar.write("No data yet.")

if "messages" not in st.session_state: st.session_state.messages=[]
for msg in st.session_state.messages:
    with st.chat_message(msg.get("role","assistant")):
        st.markdown(msg.get("content",""))
        md=msg.get("metadata")
        if md:
            with st.expander("Metadata"): st.json(md)

def _ensure_title(first_user_text: str):
    if st.session_state.thread.thread_name=="Untitled":
        st.session_state.thread.thread_name=(first_user_text or "Untitled")[:60].strip() or "Untitled"

def _append(role: str, content: str, metadata: Optional[Dict[str, Any]]=None):
    item={"role":role,"content":content,"timestamp":datetime.now().isoformat()}
    if metadata: item["metadata"]=metadata
    st.session_state.messages.append(item)
    st.session_state.thread.messages.append(item)

prompt = st.chat_input("Type your message… (Enter to send, Shift+Enter for newline)")
if prompt:
    user_intent=classify_intent(prompt); user_emotion=classify_emotion(prompt)
    _ensure_title(prompt); _append("user",prompt,{"intent":user_intent,"emotion":user_emotion})

    messages_for_api=_build_messages(st.session_state.messages, st.session_state.thread.memory_messages_number)
    if show_context_preview: st.expander("Context preview").json(messages_for_api)

    assistant_text=""; error_note=None
    try:
        llm_text=_call_openrouter(st.session_state.thread.model, st.session_state.thread.temperature, messages_for_api)
        assistant_text=babbelize(llm_text) if True else llm_text
    except Exception as e:
        error_note=str(e)
        assistant_text=f"⚠️ Error: {error_note}\n\nHint: On 401, ensure your key is a server key or the Site URL exactly matches the key's allowed domain."
    ai_intent=classify_intent(assistant_text); ai_emotion=classify_emotion(assistant_text)
    node_guidance=apply_node_rules(assistant_text, ai_emotion, ai_intent)
    if any(w in prompt.lower() for w in ("maybe","just","kinda","sort of")) and not any(w in assistant_text.lower() for w in ("maybe","just","kinda","sort of")):
        cshift_expl="Softened/hedged phrasing was normalized to direct language to avoid misinterpretation across cultures."
    else:
        cshift_expl="No cultural shifts detected beyond tone normalization."
    md={"intent":ai_intent,"emotion":ai_emotion,"node_guidance":node_guidance,"style_applied":True,"cultural_shift_explanation":cshift_expl,"error":error_note}
    _append("assistant",assistant_text,md)
    try: log_interaction(prompt, user_emotion, user_intent, "openrouter", assistant_text)
    except Exception: pass
    try: st.session_state.thread.save(SESSIONS_DIR)
    except Exception: pass
