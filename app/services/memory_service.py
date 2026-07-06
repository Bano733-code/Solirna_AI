from sqlalchemy.orm import Session
from app.models.chat_memory import ChatMemory
from app.services.embedding_service import create_embedding
from app.services.qdrant_service import store_memory


def save_memory(db: Session, user_id: int, user_message: str, ai_response: str):

    text = f"User: {user_message}\nAssistant: {ai_response}"

    embedding = create_embedding(text)

    # Store ONLY metadata in Postgres
    memory = ChatMemory(
        user_id=user_id,
        user_message=user_message,
        ai_response=ai_response
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    # Store embedding in Qdrant
    store_memory(user_id, text, embedding)

    return memory


def get_recent_memories(db: Session, user_id: int, limit: int = 5):

    return (
        db.query(ChatMemory)
        .filter(ChatMemory.user_id == user_id)
        .order_by(ChatMemory.created_at.desc())
        .limit(limit)
        .all()
    )
