import os, re, json

def ensure_dir(d: str) -> str:
    os.makedirs(d, exist_ok=True)
    return d

def slugify(text: str, max_len: int = 48) -> str:
    t = re.sub(r"\s+", " ", str(text or "")).strip().lower()
    t = re.sub(r"[^a-z0-9 _-]", "", t)
    t = t.replace(" ", "-")
    return t[:max_len] or "untitled"

def safe_read_json(path: str, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def safe_write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
