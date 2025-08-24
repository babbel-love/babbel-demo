import re

def _soften_imperatives(text: str) -> str:
    return re.sub(r"(?i)^(pick|choose|do|ask)\b", "Consider", text)

def apply_and_explain(text: str, culture: str = "default"):
    if culture == "jp":
        softened = _soften_imperatives(text)
        explanation = "Softened direct command for Japanese cultural tone."
    else:
        softened = text
        explanation = "Left unchanged for unknown culture."
    return softened, explanation
