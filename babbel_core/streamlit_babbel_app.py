import json, os, requests, streamlit as st

HARD_CODED_API_KEY = os.getenv("OPENROUTER_API_KEY","")

try:
    from rewrite import rewrite_tone, enforce_babbel_style
    def babbelize(txt: str) -> str:
        try: return enforce_babbel_style(rewrite_tone(txt)).strip()
        except: return txt
except:
    def babbelize(txt: str) -> str: return txt

def load_speech():
    try: return json.load(open("speech_protocols.json", encoding="utf-8"))
    except: return {}
SPEECH = load_speech()

def quick_protocol(msg: str):
    t = msg.lower().strip()
    if any(x in t for x in ("hi","hello","hey")) and "greeting" in SPEECH: return SPEECH["greeting"]
    if "help" in t and "help" in SPEECH: return SPEECH["help"]
    if "thanks" in t and "thank" in t and "thanks" in SPEECH: return SPEECH["thanks"]
    if any(x in t for x in ("bye","goodbye","later")) and "farewell" in SPEECH: return SPEECH["farewell"]
    return None

st.set_page_config(page_title="Babbel Core — Streamlit (OpenRouter)", page_icon="🧠", layout="centered")
st.title("🧠 Babbel Core — Streamlit + OpenRouter")


st.caption("Session chat with memory and OpenRouter backend.")

st.sidebar.header("Model & Memory")
model = st.sidebar.text_input("Model ID", value="openrouter/auto")
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.3, 0.1)
context_turns = st.sidebar.slider("Context turns", 1, 30, 10, 1)
use_babbel_style = st.sidebar.checkbox("Apply Babbel style", value=True)
show_context_preview = st.sidebar.checkbox("Show context preview", value=False)

col1,col2 = st.sidebar.columns(2)
if col1.button("Clear chat"): st.session_state.pop("messages", None); st.rerun()
if col2.button("Load greetings"):
    st.session_state.setdefault("messages",[]).append({"role":"assistant","content":SPEECH.get("greeting","Hi—how can I help?")})
    st.rerun()

st.sidebar.markdown("---")
masked = ("✔︎ " + "*" * min(12,len(HARD_CODED_API_KEY))) if HARD_CODED_API_KEY else "✖︎ missing"
st.sidebar.write(f"API key: {masked}")

try:
    from memory_tracker import log_interaction, get_recent_emotions
except:
    def log_interaction(*a,**k): pass
    def get_recent_emotions(n=10): return []
st.sidebar.header("🧭 Emotional Trajectory")
st.sidebar.write(", ".join(get_recent_emotions(10)) or "No history yet.")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
SYSTEM_PROMPT = ("You are Babbel. Respond concisely, concretely, and without filler. "
                 "Be direct, specific, and pragmatic. Avoid hedges like 'maybe'/'just'.")

def _headers():
    return {
        "Authorization": f"Bearer {HARD_CODED_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "Babbel Core (Streamlit)",
        "HTTP-Referer": "http://localhost:8501/",
    }

def ping_models():
    try:
        r = requests.get("https://openrouter.ai/api/v1/models", headers=_headers(), timeout=30)
        ok = r.status_code == 200
        body = r.json() if "application/json" in r.headers.get("Content-Type","") else r.text
        return ok, r.status_code, body
    except Exception as e:
        return False, -1, f"{type(e).__name__}: {e}"

if st.sidebar.button("Ping OpenRouter"):
    ok, code, body = ping_models()
    if ok:
        st.sidebar.success("OpenRouter reachable ✅")
        if isinstance(body, dict): st.sidebar.json(body)
        else: st.sidebar.write(str(body)[:800])
    else:
        st.sidebar.error(f"Ping failed (code {code})")
        st.sidebar.write(body if isinstance(body,str) else str(body))

def build_messages_with_context(history,n_pairs):
    msgs=[{"role":"system","content":SYSTEM_PROMPT}]
    for m in history[-(n_pairs*2):]:
        role=m.get("role","user"); content=str(m.get("content",""))[:4000]
        msgs.append({"role":role,"content":content})
    return msgs

def call_openrouter(messages):
    r=requests.post(OPENROUTER_URL,headers=_headers(),json={"model":model,"messages":messages,"temperature":temperature},timeout=90)
    if r.status_code>=400: raise RuntimeError(f"OpenRouter error {r.status_code}: {r.text}")
    return r.json()["choices"][0]["message"]["content"]

if "messages" not in st.session_state: st.session_state.messages=[]
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

prompt=st.chat_input("Type your message…")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    quick=quick_protocol(prompt)
    if quick: assistant=quick
    else:
        msgs=build_messages_with_context(st.session_state.messages,context_turns)
        if show_context_preview: st.expander("Context preview").json(msgs)
        try: llm=call_openrouter(msgs); assistant=babbelize(llm) if use_babbel_style else llm
        except Exception as e: assistant=f"⚠️ Error: {e}"
    st.session_state.messages.append({"role":"assistant","content":assistant})
    with st.chat_message("assistant"): st.markdown(assistant)
    try: log_interaction(prompt,"n/a","n/a","openrouter",assistant)
    except: pass
    st.sidebar.subheader("Latest trajectory")
    st.sidebar.write(", ".join(get_recent_emotions(5)))