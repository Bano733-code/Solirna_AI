from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user
from app.models.prd import PRD
from app.models.user import User

from app.schemas.prd import PRDRequest, PRDResponse

from app.agents.doc_agent import run_doc_agent

router = APIRouter(
    prefix="/prd",
    tags=["PRD"]
)


# ----------------------------
# Create PRD
# ----------------------------
@router.post("/", response_model=PRDResponse)
def create_prd(
    request: PRDRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    user_message = f"""
Title: {request.title}

Idea: {request.idea}
"""

    prd_text = run_doc_agent(
        user_message=user_message,
        doc_type="PRD"
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


# ----------------------------
# Get All PRDs
# ----------------------------
@router.get("/")
def get_prds(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    prds = (
        db.query(PRD)
        .filter(PRD.user_id == current_user.id)
        .order_by(PRD.created_at.desc())
        .all()
    )

    return {
        "prds": prds
    }


# ----------------------------
# Delete PRD
# ----------------------------
@router.delete("/{prd_id}")
def delete_prd(
    prd_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    prd = (
        db.query(PRD)
        .filter(
            PRD.id == prd_id,
            PRD.user_id == current_user.id
        )
        .first()
    )

    if prd is None:
        raise HTTPException(
            status_code=404,
            detail="PRD not found"
        )

    db.delete(prd)
    db.commit()

    return {
        "message": "PRD deleted successfully"
    }
