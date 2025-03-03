# schemas/ai_request_schemas.py
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AIRequestBase(BaseModel):
    input: str
    model: str

class AIRequestCreate(AIRequestBase):
    user_id: int  # Indica l'ID dell'utente che fa la richiesta

class AIRequestRead(AIRequestBase):
    id: int
    output: Optional[str] = None

    # Pydantic 2.0 style
    model_config = ConfigDict(from_attributes=True)
