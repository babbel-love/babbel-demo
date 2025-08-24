import streamlit as st
import uuid
import os
import json

SESSION_DIR = "saved_sessions"

def save_current_session():
    os.makedirs(SESSION_DIR, exist_ok=True)
    sid = st.session_state.get("session_id") or uuid.uuid4().hex
    st.session_state["session_id"] = sid
    path = os.path.join(SESSION_DIR, f"{sid}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)

def list_saved_sessions():
    if not os.path.isdir(SESSION_DIR): return []
    return [f.replace(".json", "") for f in os.listdir(SESSION_DIR) if f.endswith(".json")]

def load_session(sid):
    path = os.path.join(SESSION_DIR, f"{sid}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            st.session_state.messages = json.load(f)
            st.session_state["session_id"] = sid
