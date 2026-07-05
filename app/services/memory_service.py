from sqlalchemy.orm import Session

from app.models.chat_memory import ChatMemory
from app.services.embedding_service import create_embedding


def save_memory(
    db: Session,
    user_id: int,
    user_message: str,
    ai_response: str
):
    """
    Save a conversation along with its embedding.
    """

    text = f"User: {user_message}\nAssistant: {ai_response}"

    embedding = create_embedding(text)

    memory = ChatMemory(
        user_id=user_id,
        user_message=user_message,
        ai_response=ai_response,
        embedding=embedding
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory


def get_recent_memories(
    db: Session,
    user_id: int,
    limit: int = 5
):
    """
    Return the user's most recent conversations.
    """

    memories = (
        db.query(ChatMemory)
        .filter(ChatMemory.user_id == user_id)
        .order_by(ChatMemory.created_at.desc())
        .limit(limit)
        .all()
    )

    return memories
