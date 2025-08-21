from __future__ import annotations
import csv, os, time

def export_csv(messages, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["role","text","emotion","tone","intent","node"])
        for m in messages:
            md = m.get("metadata") or {}
            w.writerow([m.get("role",""), m.get("text",""),
                        md.get("emotion",""), md.get("tone",""), md.get("intent",""), md.get("node","")])
    return path

def export_txt(messages, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for m in messages:
            f.write(f"{m.get('role','').upper()}: {m.get('text','')}\n\n")
    return path

def default_paths():
    ts = time.strftime("%Y-%m-%d_%H-%M-%S")
    base = os.path.expanduser("~/Downloads/Babbel_Exports")
    return (os.path.join(base, f"session_{ts}.csv"), os.path.join(base, f"session_{ts}.txt"))
