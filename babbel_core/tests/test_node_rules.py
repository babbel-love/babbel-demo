from ..node_rules import apply_node_rules

def test_node_shame_confession():
    msg = "I feel disgusting and I know it’s my fault"
    out = apply_node_rules(msg, "shame", "confession")
    assert "not because it’s true" in out.lower()

def test_node_grief_search():
    msg = "Why does it hurt so much?"
    out = apply_node_rules(msg, "grief", "search for meaning")
    assert "proof that something mattered" in out.lower()
