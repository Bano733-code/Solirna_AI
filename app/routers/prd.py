from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user
from app.models.prd import PRD
from app.models.user import User

from app.schemas.prd import PRDRequest, PRDResponse

# ✅ NEW: agent import (NOT service anymore)
from app.agents.doc_agent import run_doc_agent

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

    # STEP 1: build input for agent
    user_message = f"""
Title: {request.title}

Idea: {request.idea}
"""

    # STEP 2: call doc agent (PRD generator)
    prd_text = run_doc_agent(
        user_message=user_message,
        doc_type="PRD"
    )

    # STEP 3: store in DB
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
