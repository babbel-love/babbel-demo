def classify_node(text: str) -> str:
    lowered = text.lower()
    if 'worthless' in lowered or 'no point' in lowered: return 'Collapsed Despair'
    if 'need to fix' in lowered or 'must act' in lowered: return 'Embodied Agency'
    if 'why even try' in lowered: return 'Resigned Hopelessness'
    return 'Unspecified Node'
