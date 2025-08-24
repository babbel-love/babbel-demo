import json

class NodeRewriterV2:
    def __init__(self, rewrite_rules_file='node_response_rules.json'):
        self.rewrite_rules_file = rewrite_rules_file
        self.load_rewrite_rules()

    def load_rewrite_rules(self):
        with open(self.rewrite_rules_file, 'r') as file:
            self.rewrite_rules = json.load(file)

    def rewrite_node(self, message):
        for rule in self.rewrite_rules:
            if rule['trigger'].lower() in message.lower():
                return rule['response']
        return message
