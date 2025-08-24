import streamlit as st
import os
import json

from babbel_core.pipeline import run_pipeline
from babbel_core.memory_tracker import log_interaction, get_recent_emotions
from babbel_core.intent_classifier import classify_intent
from babbel_core.emotion_classifier import classify_emotion
from babbel_core.node_rules import apply_node_rules

# ========== Page Config ==========
st.set_page_config(page_title="Babbel", layout="centered", page_icon="🧠")
st.title("🧠 Babbel Chat (Streamlit)")
st.caption("Real-time protocol-aware assistant with emotion & intent memory")

# ========== Sidebar ==========
st.sidebar.header("Settings")

model_id = st.sidebar.text_input("Model", value="openrouter/auto")
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.3, 0.1)
context_turns = st.sidebar.slider("Context turns", 1, 30, 10)

use_babbel_style = st.sidebar.checkbox("Babbel Style", value=True)
show_metadata = st.sidebar.checkbox("Show Emotion/Intent", value=True)

st.sidebar.markdown("---")
st.sidebar.subheader("Recent Emotions")
recent = get_recent_emotions(8)
st.sidebar.write(", ".join(recent) if recent else "No history yet")

# ========== Session State ==========
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{role, content, emotion, intent}]

# ========== Chat History Display ==========
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if show_metadata and msg["role"] == "assistant":
            st.caption(f"Emotion: **{msg.get('emotion','?')}** | Intent: **{msg.get('intent','?')}**")

# ========== Input Box ==========
user_input = st.chat_input("Type your message...")

if user_input:
    # User message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run Babbel
    reply_text = run_pipeline(user_input)

    # Classify metadata
    emotion = classify_emotion(user_input)
    intent = classify_intent(user_input)
    final_reply = apply_node_rules(user_input, emotion, intent)

    # Assistant message
    reply_block = {
        "role": "assistant",
        "content": final_reply,
        "emotion": emotion,
        "intent": intent
    }

    st.session_state.messages.append(reply_block)

    with st.chat_message("assistant"):
        st.markdown(final_reply)
        if show_metadata:
            st.caption(f"Emotion: **{emotion}** | Intent: **{intent}**")

    # Log interaction
    try:
        log_interaction(user_input, emotion, intent, "pipeline", final_reply)
    except:
        pass
