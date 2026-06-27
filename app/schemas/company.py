from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ----------------------------
# Create Company
# ----------------------------
class CompanyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    industry: Optional[str] = None


# ----------------------------
# Response
# ----------------------------
class CompanyResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    industry: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True