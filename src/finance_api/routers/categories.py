from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..auth import get_current_user
from ..models import Category
from ..schemas import CategoryCreate, CategoryRead

router = APIRouter()


@router.post("/", response_model=CategoryRead)
def create_category(
    payload: CategoryCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    # Check duplicate names for same user
    stmt = select(Category).where(
        Category.user_id == user.id,
        Category.name == payload.name
    )
    exists = session.exec(stmt).first()
    if exists:
        raise HTTPException(status_code=400, detail="Category name already exists")

    category = Category(
        user_id=user.id,
        name=payload.name,
        type=payload.type
    )

    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.get("/", response_model=list[CategoryRead])
def list_categories(
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    stmt = select(Category).where(Category.user_id == user.id)
    return session.exec(stmt).all()


@router.get("/{cat_id}", response_model=CategoryRead)
def get_category(
    cat_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    category = session.get(Category, cat_id)
    if not category or category.user_id != user.id:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{cat_id}", response_model=CategoryRead)
def update_category(
    cat_id: int,
    payload: CategoryCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    category = session.get(Category, cat_id)
    if not category or category.user_id != user.id:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = payload.name
    category.type = payload.type

    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.delete("/{cat_id}")
def delete_category(
    cat_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    category = session.get(Category, cat_id)
    if not category or category.user_id != user.id:
        raise HTTPException(status_code=404, detail="Category not found")

    session.delete(category)
    session.commit()
    return {"deleted": True}
