from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
#from app.dependencies import get_current_user
from app.security import get_current_user
from app.models.prd import PRD
from app.models.user import User

from app.schemas.prd import (
    PRDRequest,
    PRDResponse
)

from app.services.ai_service import generate_prd

router = APIRouter(
    prefix="/prd",
    tags=["PRD"]
)


@router.post("/", response_model=PRDResponse)
def create_prd(
    request: PRDRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    prd_text = generate_prd(
        request.title,
        request.idea
    )

    prd = PRD(
        title=request.title,
        idea=request.idea,
        generated_prd=prd_text,
        user_id=current_user.id
    )

    db.add(prd)
    db.commit()
    db.refresh(prd)

    return prd