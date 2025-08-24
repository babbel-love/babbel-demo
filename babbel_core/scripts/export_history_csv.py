#!/usr/bin/env python3
from __future__ import annotations
import csv, json
from pathlib import Path
from babbel_core.core.config import load

def main():
    cfg = load()
    out_path = Path("memory_export.csv")
    mem = Path(cfg.MEMORY_FILE)
    data = []
    if mem.exists():
        try:
            data = json.loads(mem.read_text(encoding="utf-8"))
        except Exception:
            data = []
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ts","emotion","intent","user_input","response"])
        for row in data:
            w.writerow([row.get("ts",""), row.get("emotion",""), row.get("intent",""), row.get("user_input",""), row.get("response","")])
    print(f"✅ Exported {len(data)} rows -> {out_path}")

if __name__ == "__main__":
    main()
