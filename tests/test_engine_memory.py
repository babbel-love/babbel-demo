from babbel.core.engine_memory import BabbelEngineMemory
def test_send_updates_memory():
    engine = BabbelEngineMemory()
    engine.memory = {"anchor": "start", "node": "Collapse", "emotion": "Shame"}
    resp = engine.send("I feel stuck", strict=True)
    assert resp["text"] == "Processed with anchored memory and retry check."
    assert engine.memory["anchor"] == "latest"
    assert engine.memory["node"] == "Collapse"
    assert engine.memory["emotion"] == "Shame"
