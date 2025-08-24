from node_rules import NODE_REWRITE_RULES

class NodeRewriterV2:
    def __init__(self):
        self.rules = NODE_REWRITE_RULES

    def rewrite_node(self, text: str) -> str:
        lowered = text.lower()
        for node, rule in self.rules.items():
            if any(trigger in lowered for trigger in rule.get("triggers", [])):
                return rule.get("replacement", text)
        return text
