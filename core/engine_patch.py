def export_csv(self, session_id=None, path=None):
    import os, json
    sid = session_id or self.session_id
    assert sid
    with open(os.path.join(SESS_DIR, f"{sid}.json"), "r", encoding="utf-8") as f:
        j = json.load(f)
    rows = []
    for m in j.get("messages", []):
        if m.get("role") == "assistant":
            rows.append({
                "role": m.get("role"),
                "text": m.get("text"),
                "emotion": m.get("meta", {}).get("emotion"),
                "tone": m.get("meta", {}).get("tone"),
                "node": m.get("meta", {}).get("node"),
                "cultural_explanation": m.get("meta", {}).get("cultural_explanation")
            })
    return rows
