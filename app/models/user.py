from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, index=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Relationship
    company = relationship(
        "Company",
        back_populates="users"
    )
    memories = relationship(
    "ChatMemory",
    back_populates="user",
    cascade="all, delete-orphan"
)