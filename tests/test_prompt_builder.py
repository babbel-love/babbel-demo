import importlib

ANCHOR = "# Babbel Protocol (Enforced)"

def test_build_messages_prepends_babbel_system_prompt():
    pb = importlib.import_module("babbel.engine.prompt_builder")
    assert hasattr(pb, "build_messages")
    msgs = pb.build_messages("hello world")
    assert isinstance(msgs, list) and msgs
    assert msgs[0]["role"] == "system"
    content = msgs[0].get("content") or ""
    assert ANCHOR in content
    roles = [m["role"] for m in msgs[:2]]
    assert roles[0] == "system" and "user" in roles[1]
