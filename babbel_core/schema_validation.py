from pydantic import BaseModel

class FinalOutputSchema(BaseModel):
    final_text: str
    tokens_used: int
    summary: str

def validate_final_output(data: dict) -> FinalOutputSchema:
    return FinalOutputSchema(**data)
