from pydantic import BaseModel
from datetime import datetime


class PitchDeckRequest(BaseModel):
    title: str
    startup_idea: str


class PitchDeckResponse(BaseModel):
    id: int
    title: str
    generated_pitch: str
    created_at: datetime

    class Config:
        from_attributes = True