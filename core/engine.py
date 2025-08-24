import json,os,time,uuid,csv
from . import orchestrator
SESS_DIR="sessions"
os.makedirs(SESS_DIR,exist_ok=True)
def _slug(s):
    k=" ".join(s.strip().split())[:50]
    return "".join(ch for ch in k if ch.isalnum() or ch in ("-","_"," ")).strip().replace(" ","_").lower() or "session"
class BabbelEngine:
    def __init__(self,model="openrouter/auto",tone="direct"):
        self.model=model
        self.tone=tone
        self.session_id=None
        self._messages=[]
    def _ensure_session(self,first_user_text):
        if self.session_id: return
        name=_slug(first_user_text)
        self.session_id=f"{int(time.time())}_{name}_{uuid.uuid4().hex[:6]}"
        self._save_index(name)
        self._persist()
    def _persist(self):
        path=os.path.join(SESS_DIR,f"{self.session_id}.json")
        data={"id":self.session_id,"model":self.model,"tone":self.tone,"messages":self._messages}
        with open(path,"w",encoding="utf-8") as f: json.dump(data,f,ensure_ascii=False,indent=2)
    def _save_index(self,title):
        idx=os.path.join(SESS_DIR,"index.json")
        try:
            with open(idx,"r",encoding="utf-8") as f: j=json.load(f)
        except Exception:
            j={"sessions":[]}
        j["sessions"]=[x for x in j.get("sessions",[]) if x.get("id")!=self.session_id]
        j["sessions"].append({"id":self.session_id,"title":title,"ts":int(time.time())})
        with open(idx,"w",encoding="utf-8") as f: json.dump(j,f,ensure_ascii=False,indent=2)
    def reply(self,user_text):
        assert isinstance(user_text,str) and user_text.strip()
        self._ensure_session(user_text)
        self._messages.append({"role":"user","text":user_text,"ts":int(time.time())})
        text,meta=orchestrator.respond(user_text,model=self.model,tone=self.tone)
        self._messages.append({"role":"assistant","text":text,"meta":meta,"ts":int(time.time())})
        self._persist()
        return {"text":text,"metadata":meta}
    def undo_last(self):
        if self._messages and self._messages[-1]["role"]=="assistant": self._messages.pop()
        if self._messages and self._messages[-1]["role"]=="user": self._messages.pop()
        self._persist()
    def duplicate_session(self):
        if not self.session_id: return None
        new=f"{self.session_id}_copy"
        src=os.path.join(SESS_DIR,f"{self.session_id}.json")
        dst=os.path.join(SESS_DIR,f"{new}.json")
        with open(src,"r",encoding="utf-8") as f: j=json.load(f)
        j["id"]=new
        with open(dst,"w",encoding="utf-8") as f: json.dump(j,f,ensure_ascii=False,indent=2)
        self.session_id=new
        self._save_index(j["messages"][0]["text"] if j.get("messages") else "session_copy")
        return new
    def delete_session(self,session_id=None):
        sid=session_id or self.session_id
        if not sid: return
        try: os.remove(os.path.join(SESS_DIR,f"{sid}.json"))
        idx=os.path.join(SESS_DIR,"index.json")
        try:
            with open(idx,"r",encoding="utf-8") as f: j=json.load(f)
        except Exception:
            j={"sessions":[]}
        j["sessions"]=[x for x in j.get("sessions",[]) if x.get("id")!=sid]
        with open(idx,"w",encoding="utf-8") as f: json.dump(j,f,ensure_ascii=False,indent=2)
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
