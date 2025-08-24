import os
import json
import shutil
import uuid
import pytest
import streamlit as st

from session_controls import save_current_session, list_saved_sessions, load_session

TEST_DIR = "test_sessions"

@pytest.fixture(autouse=True)
def setup_and_teardown():
    os.makedirs(TEST_DIR, exist_ok=True)
    st.session_state.clear()
    st.session_state["messages"] = [{"role": "user", "content": "hello"}]
    st.session_state["session_id"] = str(uuid.uuid4().hex)
    yield
    shutil.rmtree(TEST_DIR, ignore_errors=True)

def test_save_and_list_session(monkeypatch):
    monkeypatch.setattr("session_controls.SESSION_DIR", TEST_DIR)
    save_current_session()
    sessions = list_saved_sessions()
    assert len(sessions) == 1
    assert sessions[0] == st.session_state["session_id"]

def test_load_session(monkeypatch):
    monkeypatch.setattr("session_controls.SESSION_DIR", TEST_DIR)
    save_current_session()
    sid = st.session_state["session_id"]
    st.session_state["messages"] = []
    load_session(sid)
    assert st.session_state["messages"] == [{"role": "user", "content": "hello"}]
