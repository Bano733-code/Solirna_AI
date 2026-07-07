from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ----------------------------
# Create User
# ----------------------------
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


# ----------------------------
# Update User
# ----------------------------
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


# ----------------------------
# Response
# ----------------------------
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    company_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
