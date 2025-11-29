from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from datetime import datetime

from ..db import get_session
from ..auth import get_current_user
from ..models import Transaction, Category, Account

router = APIRouter()


def month_range(year: int, month: int):
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)
    return start, end


@router.get("/monthly")
def monthly_summary(
    year: int,
    month: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    start, end = month_range(year, month)

    stmt = select(Transaction).where(
        Transaction.user_id == user.id,
        Transaction.timestamp >= start,
        Transaction.timestamp < end
    )

    transactions = session.exec(stmt).all()

    income = sum(t.amount for t in transactions if t.amount > 0)
    expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
    net = income - expenses

    return {
        "year": year,
        "month": month,
        "income": income,
        "expenses": expenses,
        "net": net,
        "count": len(transactions),
    }


@router.get("/by-category")
def category_breakdown(
    year: int,
    month: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    start, end = month_range(year, month)

    # Fetch transactions for this month
    stmt = select(Transaction).where(
        Transaction.user_id == user.id,
        Transaction.timestamp >= start,
        Transaction.timestamp < end
    )
    transactions = session.exec(stmt).all()

    breakdown = {
        "income": {},
        "expense": {}
    }

    # Everything is "Uncategorized" for now
    for t in transactions:
        type_key = "income" if t.amount > 0 else "expense"
        category_name = "Uncategorized"

        if category_name not in breakdown[type_key]:
            breakdown[type_key][category_name] = 0

        breakdown[type_key][category_name] += abs(t.amount)

    return {
        "year": year,
        "month": month,
        "breakdown": breakdown
    }



@router.get("/balances")
def account_balances(
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    stmt = select(Account).where(Account.user_id == user.id)
    accounts = session.exec(stmt).all()

    return [
        {
            "id": acc.id,
            "name": acc.name,
            "type": acc.type,
            "balance": acc.balance
        }
        for acc in accounts
    ]


@router.get("/recent")
def recent_transactions(
    limit: int = 10,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    stmt = (select(Transaction)
            .where(Transaction.user_id == user.id)
            .order_by(Transaction.timestamp.desc())
            .limit(limit))

    transactions = session.exec(stmt).all()

    return [
        {
            "id": tx.id,
            "amount": tx.amount,
            "description": tx.description,
            "timestamp": tx.timestamp,
            "type": tx.type,
        }
        for tx in transactions
    ]
