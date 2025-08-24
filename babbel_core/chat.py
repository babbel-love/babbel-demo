import os, requests
from types import SimpleNamespace

HARD_CODED_API_KEY = os.getenv("OPENROUTER_API_KEY","")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL_ALIASES = {
    "gpt-4o-mini": "openai/gpt-4o-mini",
    "gpt-4o": "openai/gpt-4o",
}

SYSTEM_PROMPT = (
    "You are Babbel. Respond concisely, concretely, and without filler. "
    "Be direct, specific, and pragmatic. Avoid hedges like 'maybe'/'just'. "
    "When helpful, provide short steps or a crisp summary. "
    "If the user asks for recent facts, be explicit about uncertainty."
)

def _coerce_model(model_name: str) -> str:
    if not model_name: return "openrouter/auto"
    return MODEL_ALIASES.get(model_name, model_name)

def _prepare_content(part):
    if isinstance(part, str): return {"type":"text","text":part}
    if isinstance(part, dict):
        if part.get("type") in ("text","image_url"): return part
        if "image_url" in part and isinstance(part["image_url"],dict): return {"type":"image_url","image_url":part["image_url"]}
        if "text" in part and isinstance(part["text"],str): return {"type":"text","text":part["text"]}
    return {"type":"text","text":str(part)}

def _thread_messages_to_openrouter(thread_dict: dict) -> list:
    msgs=[{"role":"system","content":SYSTEM_PROMPT}]
    history=thread_dict.get("messages",[])
    max_pairs=int(thread_dict.get("memory_messages_number") or 10)
    for m in history[-(max_pairs*2):]:
        role=m.get("role","user"); content=m.get("content","")
        if isinstance(content,list): parts=[_prepare_content(p) for p in content]; msgs.append({"role":role,"content":parts})
        else: msgs.append({"role":role,"content":str(content)})
    return msgs

def use_chat(thread_dict: dict) -> dict:
    model=_coerce_model(thread_dict.get("model") or "openrouter/auto")
    temperature=float(thread_dict.get("temperature") or 0.0)
    headers={"Authorization":f"Bearer {HARD_CODED_API_KEY}","Content-Type":"application/json",
             "X-Title":"Babbel Conversation Test","HTTP-Referer":"http://localhost/"}
    payload={"model":model,"messages":_thread_messages_to_openrouter(thread_dict),"temperature":temperature}
    r=requests.post(OPENROUTER_URL,headers=headers,json=payload,timeout=90)
    if r.status_code>=400:
        try: detail=r.json()
        except: detail={"error":r.text}
        raise RuntimeError(f"OpenRouter error {r.status_code}: {detail}")
    data=r.json()
    try: content=data["choices"][0]["message"]["content"]
    except: raise RuntimeError(f"Unexpected API response shape: {data}")
    return {"messages":[SimpleNamespace(role="assistant",content=content)]}
