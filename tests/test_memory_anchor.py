from babbel.core import memory_anchor

def test_attach_memory_anchor_inserts_block():
    msgs = [{"role": "user", "content": "I'm stuck"}]
    mem = {"anchor": "prior_session", "node": "Despair", "emotion": "Shame"}
    result = memory_anchor.attach_memory_anchor(msgs, mem)
    assert result[0]["role"] == "system"
    assert "Despair" in result[0]["content"]
    assert "Shame" in result[0]["content"]
    assert result[1]["content"] == "I'm stuck"
