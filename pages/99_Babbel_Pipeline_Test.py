import os, uuid
import streamlit as st

# Prefer babbel_core; fall back to core
try:
    from babbel_core.pipeline import run_pipeline
except Exception:
    from core.pipeline import run_pipeline  # type: ignore

# Thread
ThreadCls = None
for mod in ("babbel_core.thread","core.thread"):
    try:
        ThreadCls = __import__(mod, fromlist=["ConversationThread"]).ConversationThread
        break
    except Exception:
        continue

# Memory: prefer your existing memory_tracker, else fallback to simple store
def _mem_load(session_id: str):
    # Try memory_tracker
    try:
        import babbel_core.memory_tracker as mt
        for name in ("load","read","load_session","get_session"):
            fn = getattr(mt, name, None)
            if callable(fn):
                return fn(session_id)
        # Common pattern: mt.MemoryTracker().load(session_id)
        for name in ("MemoryTracker","Tracker","Store"):
            cls = getattr(mt, name, None)
            if cls:
                try:
                    return cls().load(session_id)
                except Exception:
                    pass
    except Exception:
        pass
    # Fallback to memory_store
    try:
        from babbel_core.memory_store import load as _load
        return _load(session_id)
    except Exception:
        return {"messages":[]}

def _mem_append(session_id: str, role: str, content: str, meta=None):
    try:
        import babbel_core.memory_tracker as mt
        for name in ("append","save","save_message","write","put"):
            fn = getattr(mt, name, None)
            if callable(fn):
                return fn(session_id, role, content, meta or {})
        for name in ("MemoryTracker","Tracker","Store"):
            cls = getattr(mt, name, None)
            if cls:
                try:
                    inst = cls()
                    if hasattr(inst,"append"):
                        return inst.append(session_id, role, content, meta or {})
                    if hasattr(inst,"save_message"):
                        return inst.save_message(session_id, role, content, meta or {})
                except Exception:
                    pass
    except Exception:
        pass
    try:
        from babbel_core.memory_store import append as _append
        return _append(session_id, role, content, meta or {})
    except Exception:
        return {}

# Guard
try:
    from babbel_core.anti_chatgpt_guard import guard_output, suggest_rewrite, strip_intro
except Exception:
    def guard_output(text: str): return {"ok": True, "issues": [], "score": 0, "matches":[]}
    def suggest_rewrite(text: str): return text
    def strip_intro(text: str): return text

st.set_page_config(page_title="Babbel Pipeline Test", page_icon="🧪", layout="centered")
st.title("🧪 Babbel Pipeline Test")
st.caption("Real babbel_core pipeline + your memory tracker + Anti-ChatGPT guard.")

colA, colB, colC = st.columns(3)
with colA:
    memory_on = st.toggle("Memory", value=True)
with colB:
    strict_guard = st.toggle("Strict Guard", value=True)
with colC:
    auto_rewrite = st.toggle("Auto-rewrite on block", value=True)

st.session_state.setdefault("session_id", st.session_state.get("session_id", str(uuid.uuid4())))
session_id = st.text_input("Session ID", st.session_state["session_id"])

# Thread
if "thread" not in st.session_state:
    thread = None
    if ThreadCls:
        for args, kwargs in [
            ((), {"thread_name":"Streamlit", "model":"openrouter/auto", "temperature":0.2, "memory_messages_number":50}),
            (("Streamlit","openrouter/auto",0.2,50), {}),
            (("Streamlit",), {}),
            ((), {}),
        ]:
            try:
                thread = ThreadCls(*args, **kwargs); break
            except Exception:
                continue
    st.session_state.thread = thread

# Memory preview
if memory_on:
    doc = _mem_load(session_id)
    if doc.get("messages"):
        with st.expander("Loaded memory (last 5)"):
            for m in doc["messages"][-5:]:
                st.markdown(f"**{m.get('role','?')}**: {m.get('content','')[:300]}")

# UI history
if "messages" not in st.session_state:
    st.session_state.messages = []
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Input
user_text = st.chat_input("Type your message…")
if user_text:
    st.session_state.messages.append({"role":"user","content":user_text})
    with st.chat_message("user"):
        st.markdown(user_text)
    if memory_on:
        _mem_append(session_id, "user", user_text, {})

    # Run pipeline
    try:
        if st.session_state.thread is not None:
            raw = run_pipeline(st.session_state.thread, user_text, protocols=True)
        else:
            raw = run_pipeline(user_text)
    except TypeError:
        raw = run_pipeline(user_text)

    # Normalize
    if isinstance(raw, dict):
        text = raw.get("text") or raw.get("final_text") or raw.get("answer") or raw.get("content")
        meta = raw.get("metadata") or raw.get("scores") or {}
    else:
        text, meta = str(raw), {}

    # Guard
    guard = guard_output(text or "")
    blocked = strict_guard and not guard["ok"]
    rewritten = suggest_rewrite(strip_intro(text or "")) if (blocked and auto_rewrite) else None
    if rewritten and rewritten.strip():
        blocked = False

    with st.chat_message("assistant"):
        if blocked:
            st.error("Blocked by guard.")
            with st.expander("Guard details"): st.write(guard)
        else:
            st.markdown(rewritten or text or "_(no text)_")
            if guard["score"] > 0:
                st.warning(f"Guard flags: {guard['score']}")
            if meta:
                st.divider(); st.markdown("**Metadata / Scores**")
                for k, v in meta.items(): st.markdown(f"- **{k}**: {v}")

    if memory_on and not blocked:
        _mem_append(session_id, "assistant", (rewritten or text or ""), {"guard": guard, "meta": meta})
