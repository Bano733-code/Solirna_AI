from pydantic import BaseModel
from datetime import datetime


class PRDRequest(BaseModel):
    title: str
    idea: str


class PRDResponse(BaseModel):
    id: int
    title: str
    generated_prd: str
    created_at: datetime

    class Config:
        from_attributes = True