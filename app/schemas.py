from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str
    user_id: str

class ChatResponse(BaseModel):
    response: str
