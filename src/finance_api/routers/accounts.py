from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..schemas import AccountCreate, AccountRead
from ..models import Account
from ..auth import get_current_user

router = APIRouter()

# Create account
@router.post("/", response_model=AccountRead)
def create_account(
    payload: AccountCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    account = Account(
        user_id=user.id,
        name=payload.name,
        type=payload.type,
        balance=payload.balance
    )
    session.add(account)
    session.commit()
    session.refresh(account)
    return account

# Get all accounts of the user
@router.get("/", response_model=list[AccountRead])
def list_accounts(
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    stmt = select(Account).where(Account.user_id == user.id)
    accounts = session.exec(stmt).all()
    return accounts

# Get single account by ID
@router.get("/{account_id}", response_model=AccountRead)
def get_account(
    account_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    account = session.get(Account, account_id)
    if not account or account.user_id != user.id:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

# Update account
@router.put("/{account_id}", response_model=AccountRead)
def update_account(
    account_id: int,
    payload: AccountCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    account = session.get(Account, account_id)
    if not account or account.user_id != user.id:
        raise HTTPException(status_code=404, detail="Account not found")

    account.name = payload.name
    account.type = payload.type
    account.balance = payload.balance

    session.add(account)
    session.commit()
    session.refresh(account)
    return account

# Delete account
@router.delete("/{account_id}")
def delete_account(
    account_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    account = session.get(Account, account_id)
    if not account or account.user_id != user.id:
        raise HTTPException(status_code=404, detail="Account not found")

    session.delete(account)
    session.commit()
    return {"deleted": True}
