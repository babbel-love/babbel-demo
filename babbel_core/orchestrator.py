import re
HEDGE_PATTERNS=[r"\bmaybe\b",r"\bperhaps\b",r"\bjust\b",r"\bi think\b",r"\bkind of\b",r"\bsort of\b"]
def _strip_hedges(t:str)->str:
    out=t or ""
    for p in HEDGE_PATTERNS: out=re.sub(p,"",out,flags=re.IGNORECASE)
    out=re.sub(r"\s+"," ",out).strip(); out=out.replace("..","."); out=re.sub(r"\.{3,}",".",out); out=re.sub(r"\s+'","'",out)
    if out and out[0].islower(): out=out[0].upper()+out[1:]
    return out
def _intent(t:str)->str:
    s=(t or "").strip().lower()
    if s.endswith("?") or re.match(r"^(can|could|would|what|how|why|where|when|who)\b",s): return "question"
    if re.search(r"\b(thanks|thank you|appreciate it)\b",s): return "gratitude"
    if re.search(r"\b(bye|goodbye|farewell)\b",s): return "farewell"
    if re.search(r"\b(please|fix|do|create|build|make|send|write|implement|help)\b",s): return "task"
    if re.search(r"\b(hi|hello|hey)\b",s): return "greeting"
    return "statement"
def orchestrate(user_text:str,assistant_text:str):
    final=_strip_hedges(assistant_text); final=re.sub(r"^\s*maybe\s+","",final,flags=re.IGNORECASE).strip()
    return {"final_text":final,"user_meta":{"intent":_intent(user_text)},"assistant_meta":{"intent":_intent(assistant_text)}}
