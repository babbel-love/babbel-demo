from typing import Tuple,Dict,Any
try:
    from orchestrator import orchestrate
except Exception:
    def orchestrate(user_text:str,assistant_text:str)->Dict[str,Any]:
        return {"final_text":assistant_text,"user_meta":{"intent":"statement"},"assistant_meta":{"intent":"statement"}}
def respond(user_text:str,model:str="openrouter/auto",tone:str="neutral")->Tuple[str,Dict[str,Any]]:
    draft="I can help. Here is a quick plan so you can proceed."
    res=orchestrate(user_text,draft); text=res.get("final_text",draft); meta={**res.get("assistant_meta",{"intent":"statement"}),"model":model,"tone":tone}
    return text,meta
