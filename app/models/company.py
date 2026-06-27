from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), unique=True, index=True, nullable=False)

    description = Column(String, nullable=True)

    industry = Column(String(100), nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Relationship
    users = relationship(
        "User",
        back_populates="company"
    )