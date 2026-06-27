from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.security import get_current_user
from app.services.ai_service import chat_with_ai

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Chat with Solirna AI.
    """

    response = chat_with_ai(
        db=db,
        user_id=current_user.id,
        user_message=request.message,
    )

    return ChatResponse(
        response=response
    )