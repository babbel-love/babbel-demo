import json
import os, requests
import streamlit as st

HARD_CODED_API_KEY = os.getenv("OPENROUTER_API_KEY","")

from babbel_core.rewrite import rewrite_tone, enforce_babbel_style
def babbelize(txt: str) -> str:
    try:
        return enforce_babbel_style(rewrite_tone(txt)).strip()
    except Exception:
        return txt

def load_speech():
    try:
        with open("speech_protocols.json", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}
SPEECH = load_speech()

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

from babbel_core.memory_tracker import log_interaction, get_recent_emotions

st.set_page_config(page_title="Babbel Core — Streamlit (OpenRouter)", page_icon="🧠", layout="centered")
st.title("🧠 Babbel Core — Streamlit + OpenRouter")
st.caption("Original memory protocol: full session chat with a context-size slider.")

st.sidebar.header("Model & Memory")
model = st.sidebar.text_input("Model ID", value="openrouter/auto")
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.3, 0.1)
context_turns = st.sidebar.slider("Context turns (last N exchanges)", 1, 30, 10, 1)
use_babbel_style = st.sidebar.checkbox("Apply Babbel style", value=True)
show_context_preview = st.sidebar.checkbox("Show context preview", value=False)

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Clear chat"):
        st.session_state.pop("messages", None)
        st.rerun()
with col2:
    if st.button("Load greetings"):
        greeting = SPEECH.get("greeting") or "Hi—how can I help?"
        st.session_state.setdefault("messages", []).append({"role": "assistant", "content": greeting})
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("API key is hardcoded in this script. Do not share this file.")

st.sidebar.header("🧭 Emotional Trajectory")
recent = get_recent_emotions(10)
st.sidebar.write(", ".join(recent[-10:]) if recent else "No history yet — start chatting below.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are Babbel. Respond concisely, concretely, and without filler. "
    "Be direct, specific, and pragmatic. Avoid hedges like 'maybe'/'just'. "
    "When helpful, provide short steps or a crisp summary. "
    "If the user asks for recent facts, be explicit about uncertainty."
)

def build_messages_with_context(history, n_pairs: int):
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    tail = history[-(n_pairs*2):] if n_pairs > 0 else history
    for m in tail:
        role = m.get("role", "user")
        content = str(m.get("content", ""))[:4000]
        if role not in ("user", "assistant", "system"):
            role = "user"
        msgs.append({"role": role, "content": content})
    return msgs

def call_openrouter(messages):
    headers = {
        "Authorization": f"Bearer {HARD_CODED_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "Babbel Core (Streamlit)",
        "HTTP-Referer": "http://localhost:8501/",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=90)
    if resp.status_code >= 400:
        try:
            detail = resp.json()
        except Exception:
            detail = {"error": resp.text}
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {detail}")
    data = resp.json()
    return data["choices"][0]["message"]["content"]

prompt = st.chat_input("Type your message…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    quick = quick_protocol(prompt)
    if quick is not None:
        assistant_text = quick
    else:
        messages_for_api = build_messages_with_context(st.session_state.messages, context_turns)
        if show_context_preview:
            st.expander("Context preview").json(messages_for_api)
        try:
            llm_text = call_openrouter(messages_for_api)
            assistant_text = babbelize(llm_text) if use_babbel_style else llm_text
        except Exception as e:
            assistant_text = f"⚠️ Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
    with st.chat_message("assistant"):
        st.markdown(assistant_text)

    try:
        log_interaction(prompt, "n/a", "n/a", "openrouter", assistant_text)
    except Exception:
        pass

    st.sidebar.subheader("Latest trajectory")
    try:
        st.sidebar.write(", ".join(get_recent_emotions(5)))
    except Exception:
        pass
