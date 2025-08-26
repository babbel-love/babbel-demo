import os, sys, re, io, pathlib, json
from typing import List

TARGETS = [
    pathlib.Path("babbel_core/streamlit_babbel_app.py"),
    pathlib.Path("babbel_core/chat.py"),
]

SITE = os.getenv("OPENROUTER_SITE_URL", "http://localhost:8501")
TITLE = os.getenv("OPENROUTER_APP_TITLE", "Babbel Official Dev")

def ensure_import_os(text: str) -> str:
    if re.search(r'^\s*import\s+os\b', text, flags=re.M):
        return text
    # insert after first import block if present, else at top
    lines = text.splitlines(True)
    insert_idx = 0
    for i, ln in enumerate(lines):
        if ln.startswith("import ") or ln.startswith("from "):
            insert_idx = i + 1
            # keep going until end of contiguous import lines
        else:
            if i > 0 and (lines[i-1].startswith("import ") or lines[i-1].startswith("from ")):
                insert_idx = i
                break
    lines.insert(insert_idx, "import os\n")
    return "".join(lines)

def patch_headers_block(lines: List[str]) -> List[str]:
    out = []
    inside = False
    indent = ""
    has_ref = has_origin = has_xtitle = False

    def flush_missing():
        extra = []
        if not has_xtitle:
            extra.append(f'{indent}"X-Title": os.getenv("OPENROUTER_APP_TITLE", "Babbel Official Dev"),\n')
        if not has_ref:
            extra.append(f'{indent}"Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost:8501"),\n')
        if not has_origin:
            extra.append(f'{indent}"Origin": os.getenv("OPENROUTER_SITE_URL", "http://localhost:8501"),\n')
        return extra

    for ln in lines:
        if not inside:
            out.append(ln)
            if re.search(r'headers\s*=\s*\{', ln):
                inside = True
                # base indent from the headers line plus 4 spaces
                indent = re.match(r'(\s*)', ln).group(1) + "    "
                # reset flags per block
                has_ref = has_origin = has_xtitle = False
            continue

        # inside headers
        # rename legacy key
        ln = ln.replace('"HTTP-Referer"', '"Referer"')

        # track keys & normalize values
        if re.search(r'"X-Title"\s*:', ln):
            has_xtitle = True
            ln = re.sub(r'("X-Title"\s*:\s*)[^,]+', r'\1os.getenv("OPENROUTER_APP_TITLE", "Babbel Official Dev")', ln)

        if re.search(r'"Referer"\s*:', ln):
            has_ref = True
            ln = re.sub(r'("Referer"\s*:\s*)[^,]+', r'\1os.getenv("OPENROUTER_SITE_URL", "http://localhost:8501")', ln)

        if re.search(r'"Origin"\s*:', ln):
            has_origin = True
            ln = re.sub(r'("Origin"\s*:\s*)[^,]+', r'\1os.getenv("OPENROUTER_SITE_URL", "http://localhost:8501")', ln)

        out.append(ln)

        # detect end of dict (assume a closing brace alone on its line or with trailing comma)
        if re.match(r'\s*\}', ln):
            # inject any missing keys *before* this closing brace
            injected = flush_missing()
            if injected:
                # insert injected entries just before closing brace
                out[-1:-1] = injected
            inside = False

    return out

def process_file(path: pathlib.Path) -> dict:
    if not path.exists():
        return {"path": str(path), "exists": False}
    orig = path.read_text(encoding="utf-8")
    txt = ensure_import_os(orig)

    # multi-block safe: operate on entire file line-wise, patch every headers dict
    lines = txt.splitlines(True)
    new_lines = []
    i = 0
    while i < len(lines):
        if re.search(r'headers\s*=\s*\{', lines[i]):
            # collect until matching closing brace at same or lesser indent depth
            block = [lines[i]]
            i += 1
            while i < len(lines):
                block.append(lines[i])
                if re.match(r'\s*\}', lines[i]):
                    i += 1
                    break
                i += 1
            new_block = patch_headers_block(block)
            new_lines.extend(new_block)
        else:
            new_lines.append(lines[i])
            i += 1

    new_txt = "".join(new_lines)

    changed = (new_txt != orig)
    if changed:
        path.write_text(new_txt, encoding="utf-8")
    return {"path": str(path), "exists": True, "changed": changed}

def main():
    results = []
    for p in TARGETS:
        # backup
        if p.exists():
            bp = pathlib.Path("backups") / f"{p.name}.backup.$$.py"
            bp.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
        results.append(process_file(p))
    print(json.dumps({"patch_results": results}, indent=2))

if __name__ == "__main__":
    main()
