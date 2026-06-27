from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pgvector.sqlalchemy import Vector   # ✅ IMPORTANT

from app.database import Base


class ChatMemory(Base):
    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user_message = Column(Text, nullable=False)

    ai_response = Column(Text, nullable=False)

    # ✅ VECTOR EMBEDDING (RAG CORE)
    embedding = Column(Vector(384))

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship(
    "User",
    back_populates="memories"
)