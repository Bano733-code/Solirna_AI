from sqlalchemy.orm import Session

from app.models.chat_memory import ChatMemory


def save_memory(
    db: Session,
    user_id: int,
    user_message: str,
    ai_response: str,
):

    memory = ChatMemory(
        user_id=user_id,
        user_message=user_message,
        ai_response=ai_response,
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory


def get_recent_memories(
    db: Session,
    user_id: int,
    limit: int = 5,
):

    return (
        db.query(ChatMemory)
        .filter(ChatMemory.user_id == user_id)
        .order_by(ChatMemory.created_at.desc())
        .limit(limit)
        .all()
    )
