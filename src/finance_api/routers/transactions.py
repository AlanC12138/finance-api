from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..auth import get_current_user
from ..models import Account, Transaction
from ..schemas import TransactionCreate, TransactionRead

router = APIRouter()


def update_account_balance(account: Account, delta: float, session: Session):
    account.balance += delta
    session.add(account)
    session.commit()
    session.refresh(account)


@router.post("/", response_model=TransactionRead)
def create_transaction(
    payload: TransactionCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    # Validate account belongs to this user
    account = session.get(Account, payload.account_id)
    if not account or account.user_id != user.id:
        raise HTTPException(status_code=404, detail="Account not found")

    # Create transaction
    tx = Transaction(
        user_id=user.id,
        account_id=payload.account_id,
        amount=payload.amount,
        description=payload.description,
        type=payload.type
    )
    session.add(tx)

    # Update balance
    update_account_balance(account, payload.amount, session)

    session.commit()
    session.refresh(tx)
    return tx


@router.get("/", response_model=list[TransactionRead])
def list_transactions(
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    stmt = select(Transaction).where(Transaction.user_id == user.id)
    return session.exec(stmt).all()


@router.get("/{tx_id}", response_model=TransactionRead)
def get_transaction(
    tx_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    tx = session.get(Transaction, tx_id)
    if not tx or tx.user_id != user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx


@router.delete("/{tx_id}")
def delete_transaction(
    tx_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    tx = session.get(Transaction, tx_id)
    if not tx or tx.user_id != user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Reverse balance before deleting
    account = session.get(Account, tx.account_id)
    update_account_balance(account, -tx.amount, session)

    session.delete(tx)
    session.commit()
    return {"deleted": True}
