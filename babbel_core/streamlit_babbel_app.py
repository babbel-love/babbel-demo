import streamlit as st
import os
import json
from babbel_core.thread import ConversationThread
from babbel_core.pipeline import run_pipeline
from babbel_core.memory_tracker import get_recent_emotions, log_interaction

MEMORY_FILE = "babbel_core/memory_log.json"

# --- UI Setup ---
st.set_page_config(page_title="Babbel Core — Streamlit", page_icon="🧠", layout="centered")
st.title("🧠 Babbel Core — Streamlit Memory Mode")
st.caption("Full rewrite + tone + persistent memory.")

# Sidebar controls
st.sidebar.header("Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.3, 0.1)
context_turns = st.sidebar.slider("Context turns", 1, 30, 10, 1)
show_metadata = st.sidebar.checkbox("Show metadata", value=True)

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Clear chat"):
        st.session_state.pop("messages", None)
        if os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)
        st.rerun()
with col2:
    if st.button("Load greeting"):
        st.session_state.setdefault("messages", []).append({"role": "assistant", "content": "Hi—how can I help?"})
        st.rerun()

# Emotion trajectory
st.sidebar.subheader("🧭 Recent Emotions")
st.sidebar.write(", ".join(get_recent_emotions(10)) or "No history yet.")

# --- Load memory file if chat empty ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                entries = json.load(f)
                for entry in entries:
                    st.session_state.messages.append({"role": "user", "content": entry["input"]})
                    st.session_state.messages.append({"role": "assistant", "content": entry["final_reply"]})
        except Exception:
            st.warning("⚠️ Could not load memory_log.json.")

# --- Display messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Handle input ---
prompt = st.chat_input("Type your message…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    thread = ConversationThread("streamlit", "openrouter/auto", temperature, context_turns)
    for m in st.session_state.messages:
        thread.add_message(m["role"], m["content"])

    result = run_pipeline(thread, prompt)
    final = result["final_text"]

    st.session_state.messages.append({"role": "assistant", "content": final})
    with st.chat_message("assistant"):
        st.markdown(final)

    if show_metadata:
        with st.expander("Metadata"):
            st.json({
                "emotion": result["emotion"],
                "intent": result["intent"],
                "raw_response": result["raw_response"]
            })

    # Refresh sidebar emotion bar
    st.sidebar.subheader("Latest trajectory")
    st.sidebar.write(", ".join(get_recent_emotions(5)))

# === [📦 Session Save/Load] ===
import os
from thread import ConversationThread
SESSIONS_DIR = "babbel_core/sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

st.sidebar.subheader("🧵 Sessions")
session_files = sorted(f for f in os.listdir(SESSIONS_DIR) if f.endswith(".json"))

def load_session(path):
    try:
        full_path = os.path.join(SESSIONS_DIR, path)
        return ConversationThread.load(full_path)
    except Exception:
        return None

selected_file = st.sidebar.selectbox("Load session", ["(new)"] + session_files)
if selected_file != "(new)":
    loaded = load_session(selected_file)
    if loaded:
        st.session_state.messages = loaded.messages
        st.success(f"Loaded: {selected_file}")

if st.sidebar.button("💾 Save current session"):
    thread = ConversationThread("Saved via GUI", model, temperature, context_turns)
    thread.messages = st.session_state.messages
    thread.save(SESSIONS_DIR)
    st.success("Session saved.")

# === [🔍 Emotion Search] ===
st.sidebar.subheader("🔍 Search by Emotion")
search_emotion = st.sidebar.text_input("Enter emotion (e.g. shame, fear)").lower().strip()
if search_emotion:
    matches = [m for m in st.session_state.messages if search_emotion in m.get("content", "").lower()]
    st.sidebar.write(f"{len(matches)} matches")
    if matches:
        with st.expander("Matching Messages"):
            for m in matches:
                st.markdown(f"**{m['role']}**: {m['content']}")

# === [📤 Export CSV/TXT] ===
import pandas as pd
st.sidebar.subheader("📤 Export")
def export_dataframe():
    return pd.DataFrame([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])

if st.sidebar.button("Export as CSV"):
    df = export_dataframe()
    df.to_csv("babbel_export.csv", index=False)
    st.success("Exported to babbel_export.csv")

if st.sidebar.button("Export as TXT"):
    with open("babbel_export.txt", "w", encoding="utf-8") as f:
        for m in st.session_state.messages:
            f.write(f"{m['role'].upper()}: {m['content']}\n\n")
    st.success("Exported to babbel_export.txt")

# === [🪪 Rewrite Debugger] ===
from node_rewrite_v2 import NodeRewriterV2
st.markdown("---")
with st.expander("🪪 Rewrite Debugger"):
    rewriter = NodeRewriterV2()
    test_input = st.text_area("Input to test rewrite", "Can you help with my issue?")
    if st.button("Run Rewrite Debugger"):
        output = rewriter.rewrite_node(test_input)
        st.write("Rewritten Output:")
        st.success(output)

# === [📊 Emotion Graph] ===
import matplotlib.pyplot as plt
try:
    emolist = get_recent_emotions(50)
    if emolist:
        st.sidebar.subheader("📊 Emotion Graph")
        fig, ax = plt.subplots()
        ax.plot(emolist, marker='o')
        ax.set_xticks(range(len(emolist)))
        ax.set_xticklabels(range(1, len(emolist)+1), rotation=90)
        ax.set_ylabel("Emotion")
        ax.set_title("Recent Emotion Trajectory")
        st.sidebar.pyplot(fig)
except Exception:
    st.sidebar.info("No graph data yet.")

# === [🧷 Autosave every turn] ===
def autosave_session():
    thread = ConversationThread("AutoSaved", model, temperature, context_turns)
    thread.messages = st.session_state.messages
    thread.save(SESSIONS_DIR)

# After assistant_text is added (inside chat input handler):
try:
    autosave_session()
except Exception:
    pass

# === [🧷 Autosave every turn] ===
def autosave_session():
    thread = ConversationThread("AutoSaved", model, temperature, context_turns)
    thread.messages = st.session_state.messages
    thread.save(SESSIONS_DIR)

# Run autosave after assistant reply
try:
    autosave_session()
except Exception:
    pass

# === [🧠 True Rewrite Debugger — Node-Aware] ===
from emotion_classifier import classify_emotion
from intent_classifier import classify_intent
from node_rules import apply_node_rules
from rewrite import rewrite_tone, enforce_babbel_style

st.markdown("---")
with st.expander("🧠 Node-Aware Rewrite Debugger"):
    test_input = st.text_area("Try anything emotionally raw...", "I feel worthless and broken.")
    if st.button("Run Real Babbel Debugger"):
        emotion = classify_emotion(test_input)
        intent = classify_intent(test_input)
        node_text = apply_node_rules(test_input, emotion, intent)
        styled_text = enforce_babbel_style(rewrite_tone(node_text)).strip()

        st.markdown(f"**Detected Emotion:** `{emotion}`")
        st.markdown(f"**Detected Intent:** `{intent}`")

        st.markdown("**🔁 Babbel Rewrite:**")
        st.success(styled_text)

        st.markdown("**💡 Explanation:**")
        if emotion == "shame":
            st.info("This rewrite is grounded in the assumption that shame often distorts truth into unbearable self-judgment. Babbel gently reframes the emotion without invalidating it.")
        elif emotion == "grief":
            st.info("Grief isn't bypassed here — it's honored. The rewrite respects what was lost while inviting depth.")
        elif intent == "confession":
            st.info("Rather than offer advice, Babbel recognizes the need to feel seen. It offers presence instead of solutions.")
        else:
            st.info("The rewrite slows things down, offering space rather than rushing to explain or fix.")
