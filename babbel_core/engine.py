from typing import Dict
def _emo(t: str) -> str:
    tl=t.lower()
    s={"joy":0,"sadness":0,"anger":0,"fear":0,"surprise":0}
    [s.__setitem__("joy",s["joy"]+tl.count(w)) for w in ("love","great","awesome","thanks","glad","nice","cool")]
    [s.__setitem__("sadness",s["sadness"]+tl.count(w)) for w in ("sad","sorry","upset","disappoint","unhappy","regret")]
    [s.__setitem__("anger",s["anger"]+tl.count(w)) for w in ("angry","mad","furious","annoy","wtf","terrible")]
    [s.__setitem__("fear",s["fear"]+tl.count(w)) for w in ("worried","afraid","scared","fear","risk","concern")]
    [s.__setitem__("surprise",s["surprise"]+tl.count(w)) for w in ("wow","unexpected","didn't know","surprised")]
    k=max(s,key=s.get)
    return k if s[k]>0 else "neutral"
def _intent(t:str)->str:
    tl=t.strip().lower()
    if not tl: return "unknown"
    if tl.startswith(("how ","what ","why ","where ","when ","which ","who ","can ","could ","should ","do ","does ","did ","is ","are ","am ","will ","would ")):
        return "question"
    if any(k in tl for k in ("please","step-by-step","walk me through","show me","guide me","help me")): return "task"
    if any(k in tl for k in ("hi","hello","hey","good morning","good evening")): return "greeting"
    if any(k in tl for k in ("thanks","thank you","thx","appreciate")): return "gratitude"
    if any(k in tl for k in ("bye","goodbye","see you","later")): return "farewell"
    return "statement"
def _node(t:str)->str:
    e=_emo(t)
    if e in ("joy","neutral"): return "Embodied Agency"
    if e in ("sadness","fear"): return "Collapsed Despair"
    if e=="anger": return "Reactive Protest"
    return "Neutral"
def _rewrite(txt:str)->str:
    hedges=("maybe","just "," kinda"," kind of"," sort of","probably","perhaps","i think","might ","a bit","little bit")
    out=txt
    for h in hedges:
        out=out.replace(h,"").replace(h.capitalize(),"")
    return " ".join(out.split())
class BabbelEngine:
    def __init__(self):
        self.memory={"anchor":"start","node":"None","emotion":"Neutral"}
    def send(self, user_input:str, strict:bool=True)->Dict:
        em=_emo(user_input); it=_intent(user_input); nd=_node(user_input)
        raw=f"I hear you. {user_input}"
        final=_rewrite(raw)
        self.memory.update({"anchor":"latest","node":nd,"emotion":em})
        return {"text":final,"metadata":{"emotion":em,"intent":it,"node":nd}}
