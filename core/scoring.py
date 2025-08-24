def compute_scores(original: str, rewritten: str, node: str, history: list[str]) -> dict:
    return {
        'rewrite_risk': 0 if original == rewritten else 1,
        'node_clarity': 1 if node != 'Unspecified Node' else 0,
        'memory_depth': len(history),
        'fact_risk': 0 if '?' not in original else 1
    }
