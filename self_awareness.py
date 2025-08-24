import os, re, json
from typing import List, Dict, Iterable, Tuple

IGNORE_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "node_modules", "build", "dist", ".idea", ".vscode"}
MAX_FILE_SIZE = 512_000  # 512 KB cap to avoid huge binaries

def iter_files(root: str = ".") -> Iterable[str]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for f in filenames:
            p = os.path.join(dirpath, f)
            try:
                if os.path.getsize(p) > MAX_FILE_SIZE:
                    continue
                # skip obvious binaries
                with open(p, "rb") as fh:
                    head = fh.read(2048)
                if b"\x00" in head:
                    continue
            except Exception:
                continue
            yield p

def grep(pattern: str, root: str = ".") -> List[Dict[str, str]]:
    rx = re.compile(pattern, re.IGNORECASE)
    hits: List[Dict[str, str]] = []
    for p in iter_files(root):
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f, 1):
                    if rx.search(line):
                        hits.append({"file": p, "line": i, "text": line.rstrip()})
                        if len(hits) >= 500:
                            return hits
        except Exception:
            continue
    return hits

def describe_project(root: str = ".") -> Dict[str, int]:
    exts = {}
    for p in iter_files(root):
        ext = os.path.splitext(p)[1].lower() or "(none)"
        exts[ext] = exts.get(ext, 0) + 1
    return dict(sorted(exts.items(), key=lambda kv: (-kv[1], kv[0])))

def find_symbols(symbol: str, root: str = ".") -> List[Dict[str,str]]:
    # naive: look for def/class lines first, then other lines
    rx_def = re.compile(rf"\\b(class|def)\\s+{re.escape(symbol)}\\b")
    rx_any = re.compile(re.escape(symbol))
    results = []
    for p in iter_files(root):
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                data = f.read()
        except Exception:
            continue
        for rx in (rx_def, rx_any):
            for m in rx.finditer(data):
                line_no = data.count("\\n", 0, m.start()) + 1
                snippet = data.splitlines()[line_no-1][:200]
                results.append({"file": p, "line": line_no, "text": snippet})
                if len(results) >= 300:
                    return results
    return results

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Local self-awareness utility (safe, offline).")
    ap.add_argument("--grep", help="regex to search", default="")
    ap.add_argument("--symbol", help="symbol to find (def/class/name)", default="")
    ap.add_argument("--describe", action="store_true", help="summarize file types")
    args = ap.parse_args()

    out = {}
    if args.grep:
        out["grep"] = grep(args.grep)
    if args.symbol:
        out["symbols"] = find_symbols(args.symbol)
    if args.describe:
        out["summary"] = describe_project(".")
