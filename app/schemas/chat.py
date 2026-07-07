from pydantic import BaseModel
from datetime import datetime


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


class MemoryResponse(BaseModel):
    id: int
    user_message: str
    ai_response: str
    created_at: datetime

    class Config:
        from_attributes = True
class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    createdAt: str


class ChatHistoryResponse(BaseModel):
    messages: list[ChatMessageResponse]
