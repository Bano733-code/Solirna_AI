from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user
from app.models.pitchdeck import PitchDeck
from app.models.user import User
from app.schemas.pitchdeck import PitchDeckRequest, PitchDeckResponse

from app.agents.doc_agent import run_doc_agent

router = APIRouter(
    prefix="/pitchdeck",
    tags=["PitchDeck"]
)


@router.post("/", response_model=PitchDeckResponse)
def create_pitchdeck(
    request: PitchDeckRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    user_message = f"""
Startup Name: {request.title}

Idea: {request.startup_idea}
"""

    pitchdeck_text = run_doc_agent(
        user_message=user_message,
        doc_type="Pitch Deck"
    )

    pitch = PitchDeck(
        title=request.title,
        startup_idea=request.startup_idea,
        generated_pitch=pitchdeck_text,
        user_id=current_user.id
    )

    db.add(pitch)
    db.commit()
    db.refresh(pitch)

    return pitch
