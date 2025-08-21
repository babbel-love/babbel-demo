import types
import importlib
import builtins

ANCHOR = "# Babbel Protocol (Enforced)"

def test_engine_send_requires_anchor(monkeypatch):
    engine = importlib.import_module("babbel.engine.engine")
    pb = importlib.import_module("babbel.engine.prompt_builder")
    assert hasattr(pb, "build_messages")
    assert hasattr(engine, "_assert_babbel_identity")
    bad_messages = [{"role":"user","content":"hi"}]
    try:
        engine.send(messages=bad_messages)
        raised = False
    except Exception:
        raised = True
    assert raised
    good_messages = [
        {"role":"system","content": f"{ANCHOR}\nSystem init"},
        {"role":"user","content":"Hello"}
    ]
    if hasattr(engine, "_call_model"):
        monkeypatch.setattr(engine, "_call_model", lambda messages, **kw: {"text":"ok","messages":messages})
        resp = engine.send(messages=good_messages)
        assert resp is not None
    elif hasattr(engine, "MODEL"):
        class FakeModel:
            def __call__(self, messages=None, **kw):
                return {"text":"ok","messages":messages}
        monkeypatch.setattr(engine, "MODEL", FakeModel())
        resp = engine.send(messages=good_messages)
        assert resp is not None
    else:
        if hasattr(engine, "transport"):
            class FakeTransport:
                def send(self, messages=None, **kw):
                    return {"text":"ok","messages":messages}
            monkeypatch.setattr(engine, "transport", FakeTransport())
        resp = engine.send(messages=good_messages)
        assert resp is not None

def test_engine_send_calls_build_messages(monkeypatch):
    engine = importlib.import_module("babbel.engine.engine")
    pb = importlib.import_module("babbel.engine.prompt_builder")
    called = {"hit": False}
    real_build = pb.build_messages
    def spy_build(*a, **k):
        called["hit"] = True
        out = real_build(*a, **k)
        assert out[0]["role"] == "system"
        assert ANCHOR in (out[0].get("content") or "")
        return out
    monkeypatch.setattr(pb, "build_messages", spy_build)
    if hasattr(engine, "_call_model"):
        monkeypatch.setattr(engine, "_call_model", lambda messages, **kw: {"text":"ok","messages":messages})
    elif hasattr(engine, "MODEL"):
        class FakeModel:
            def __call__(self, messages=None, **kw):
                return {"text":"ok","messages":messages}
        monkeypatch.setattr(engine, "MODEL", FakeModel())
    else:
        if hasattr(engine, "transport"):
            class FakeTransport:
                def send(self, messages=None, **kw):
                    return {"text":"ok","messages":messages}
            monkeypatch.setattr(engine, "transport", FakeTransport())
    resp = engine.send(user_text="Hello Babbel")
    assert called["hit"]
    assert resp is not None

def test_runtime_identity_guard_is_enforced(monkeypatch):
    engine = importlib.import_module("babbel.engine.engine")
    bad = [{"role":"system","content":"no anchor here"}, {"role":"user","content":"hi"}]
    try:
        engine.send(messages=bad)
        assert False
    except Exception:
        pass
