from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..db import get_session
from ..models import User
from ..schemas import UserCreate, UserRead, Token
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(payload: UserCreate, session: Session = Depends(get_session)):
    # Check email exists
    statement = select(User).where(User.email == payload.email)
    user = session.exec(statement).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=payload.email,
        password_hash=hash_password(payload.password)
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(payload: UserCreate, session: Session = Depends(get_session)):
    # Find user
    stmt = select(User).where(User.email == payload.email)
    user = session.exec(stmt).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Create token with user ID as subject
    access_token = create_access_token({"sub": str(user.id)})

    return Token(access_token=access_token)
