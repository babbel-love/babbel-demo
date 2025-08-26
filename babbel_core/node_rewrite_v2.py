import json
import unicodedata
import os

class NodeRewriterV2:
    def __init__(self, rewrite_rules_file=None):
        if rewrite_rules_file is None:
            base = os.path.dirname(__file__)
            self.rewrite_rules_file = os.path.join(base, "node_response_rules.json")
        else:
            self.rewrite_rules_file = rewrite_rules_file
        self.load_rewrite_rules()

    def load_rewrite_rules(self):
        with open(self.rewrite_rules_file, 'r', encoding="utf-8") as file:
            self.rewrite_rules = json.load(file)
        print(f"[🔁 NodeRewriterV2] Loaded {len(self.rewrite_rules)} rewrite rules.")

    def normalize(self, text):
        text = unicodedata.normalize('NFKD', text)
        text = ''.join(c for c in text if not unicodedata.combining(c))
        text = text.lower().strip()
        return ''.join(c for c in text if c.isalnum() or c.isspace())

    def rewrite_node(self, message):
        normalized_msg = self.normalize(message)
        print(f"\n🔍 Rewriting attempt for: “{message}”")
        print(f"🧽 Normalized: “{normalized_msg}”")
        
        for rule in self.rewrite_rules:
            trigger = self.normalize(rule.get('trigger', ''))
            if not trigger:
                continue
            print(f"  🔹 Checking trigger: “{trigger}”")
            if trigger in normalized_msg:
                print(f"✅ MATCHED: '{trigger}' → {rule['response']}")
                return rule['response']
        
        print("🚫 No node rule matched.")
        return message

if __name__ == '__main__':
    rewriter = NodeRewriterV2()
    test_inputs = [
        "What's wrong with me?",
        "i feel worthless.",
        "Can you help with my issue?",
        "I need advice."
    ]
    for msg in test_inputs:
        out = rewriter.rewrite_node(msg)
        print(f"→ {out}")

def run_node_rewrite(text: str) -> str:
    rewriter = NodeRewriterV2()
    return rewriter.rewrite_node(text)
