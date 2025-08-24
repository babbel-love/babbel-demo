import json,os,urllib.request,urllib.error,ssl,time
DEFAULT_URL="https://openrouter.ai/api/v1/chat/completions"
def call(messages,model="openrouter/auto",url=DEFAULT_URL,timeout=30,retries=2):
    if os.getenv("BABBEL_OFFLINE")=="1":
        raise RuntimeError("offline")
    key=os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_KEY")
    if not key:
        raise RuntimeError("missing_key")
    payload={"model":model,"messages":messages}
    data=json.dumps(payload).encode("utf-8")
    headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"}
    req=urllib.request.Request(url,data=data,headers=headers,method="POST")
    ctx=ssl.create_default_context()
    last=None
    for i in range(retries+1):
        try:
            with urllib.request.urlopen(req,timeout=timeout,context=ctx) as r:
                b=r.read()
                j=json.loads(b.decode("utf-8",errors="replace"))
                t=(j.get("choices") or [{}])[0].get("message",{}).get("content","")
                return t
        except Exception as e:
            last=e
            time.sleep(min(2**i,4))
    raise RuntimeError(f"network_error:{type(last).__name__}")
