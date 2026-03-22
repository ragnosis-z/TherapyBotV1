from pydantic import BaseModel
from modes import Mode

class ChatRequest(BaseModel):
    message: str
    mode: Mode

class ChatResponse(BaseModel):
    response: str
    mode: Mode
