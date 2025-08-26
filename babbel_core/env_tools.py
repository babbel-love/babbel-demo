import os, re
from dotenv import dotenv_values

ENV_PATH = os.path.join(os.getcwd(), ".env")

def get_env_model(default_model: str="openrouter/auto") -> str:
    cfg = dotenv_values(ENV_PATH)
    return (cfg.get("OPENROUTER_MODEL") or os.getenv("OPENROUTER_MODEL") or default_model).strip()

def set_env_model(model: str) -> None:
    model = (model or "").strip()
    lines = []
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    key = "OPENROUTER_MODEL"
    found = False
    for i,ln in enumerate(lines):
        if ln.startswith(f"{key}="):
            lines[i] = f"{key}={model}"
            found = True
            break
    if not found:
        lines.append(f"{key}={model}")
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))
