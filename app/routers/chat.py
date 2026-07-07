from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.chat_memory import ChatMemory
from app.schemas.chat import ChatRequest, ChatResponse, MemoryResponse
from app.security import get_current_user
from app.services.ai_service import chat_with_ai


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


# Send message
@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    response = chat_with_ai(
        db=db,
        user_id=current_user.id,
        user_message=request.message,
    )

    return ChatResponse(
        response=response
    )


# Get chat history
@router.get("/")
def get_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    memories = db.query(ChatMemory).filter(
        ChatMemory.user_id == current_user.id
    ).order_by(
        ChatMemory.created_at.asc()
    ).all()


    messages = []

    for memory in memories:
        messages.append({
            "id": f"{memory.id}-user",
            "role": "user",
            "content": memory.user_message,
            "createdAt": memory.created_at.isoformat()
        })

        messages.append({
            "id": f"{memory.id}-assistant",
            "role": "assistant",
            "content": memory.ai_response,
            "createdAt": memory.created_at.isoformat()
        })


    return {
        "messages": messages
    }



# Delete chat history
@router.delete("/")
def delete_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    db.query(ChatMemory).filter(
        ChatMemory.user_id == current_user.id
    ).delete()


    db.commit()


    return {
        "message": "Chat history deleted successfully"
    }
