import json
import os
import streamlit as st
from babbel_core.core.orchestrator import Orchestrator
from memory_tracker import log_interaction, get_recent_emotions

engine = Orchestrator()

def load_speech():
    with open("speech_protocols.json", encoding="utf-8") as f:
        return json.load(f)
SPEECH = load_speech()

def quick_protocol(msg):
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

st.set_page_config(page_title="Babbel Core", page_icon="🧠", layout="centered")
st.title("🧠 Babbel Core")
st.caption("Full pipeline with emotional memory and tone enforcement")

st.sidebar.header("Model & Memory")
model = st.sidebar.text_input("Model ID", value="openrouter/auto")
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.3, 0.1)
context_turns = st.sidebar.slider("Context turns", 1, 30, 10, 1)
show_context_preview = st.sidebar.checkbox("Show context preview", value=False)

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Clear chat"):
        st.session_state.pop("messages", None)
        st.rerun()
with col2:
    if st.button("Load greetings"):
        greeting = SPEECH.get("greeting", "Hi—how can I help?")
        st.session_state.setdefault("messages", []).append({"role": "assistant", "content": greeting})
        st.rerun()

st.sidebar.header("🧭 Emotional Trajectory")
recent = get_recent_emotions(10)
st.sidebar.write(", ".join(recent[-10:]) if recent else "No history yet")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type your message…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    quick = quick_protocol(prompt)
    if quick:
        assistant_text = quick
    else:
        thread_dict = {
            "messages": st.session_state.messages,
            "model": model,
            "temperature": temperature,
            "memory_messages_number": context_turns
        }

        if show_context_preview:
            st.expander("Context preview").json(thread_dict)

        response = engine.send_thread(thread_dict)
        assistant_text = response["text"]

    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
    with st.chat_message("assistant"):
        st.markdown(assistant_text)

    try:
        log_interaction(
            prompt,
            response.get("metadata", {}).get("emotion", "n/a"),
            response.get("metadata", {}).get("intent", "n/a"),
            "orchestrator",
            assistant_text
        )
    except Exception:
        pass

    st.sidebar.subheader("Latest trajectory")
    try:
        st.sidebar.write(", ".join(get_recent_emotions(5)))
    except Exception:
        pass

st.markdown("---")

from session_controls import save_current_session, list_saved_sessions, load_session

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("New session"):
        st.session_state["messages"] = []
        st.session_state["session_id"] = str(uuid.uuid4().hex)
        st.rerun()
with col2:
    if st.button("Save"):
        save_current_session()

saved = list_saved_sessions()
if saved:
    st.sidebar.subheader("Load previous session")
    selected = st.sidebar.selectbox("Pick a session", saved, index=0)
    if st.sidebar.button("Load"):
        load_session(selected)
        st.rerun()
