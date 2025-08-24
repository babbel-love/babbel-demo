import json
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any, Optional
from pathlib import Path

class MessageBlock(BaseModel):
    role: str
    content: Any

class FinalOutputSchema(BaseModel):
    final_text: str
    tokens_used: int = 0
    summary: str = ""

class ThreadSchema(BaseModel):
    thread_name: str
    model: str
    temperature: float = 0.0
    memory_messages_number: int = 10
    messages: List[MessageBlock]
    thread_id: Optional[str]

def validate_final_output(data: dict) -> FinalOutputSchema:
    return FinalOutputSchema(**data)

def validate_thread_dict(data: dict | str | Path) -> dict:
    if isinstance(data, (str, Path)):
        with open(data, "r") as f:
            data = json.load(f)
    validated = ThreadSchema(**data)
    return validated.model_dump()
