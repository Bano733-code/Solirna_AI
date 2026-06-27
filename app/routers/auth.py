from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest, Token
from fastapi import APIRouter, Depends
from app.security import get_current_user

from app.security import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ----------------------------
# Register
# ----------------------------
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create user
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


# ----------------------------
# Login
# ----------------------------
@router.post("/login", response_model=Token)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == credentials.email
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        credentials.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email
        }
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )
@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return current_user
