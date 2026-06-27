from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class PitchDeck(Base):
    __tablename__ = "pitch_decks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    startup_idea = Column(Text, nullable=False)

    generated_pitch = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")