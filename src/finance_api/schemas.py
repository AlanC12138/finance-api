from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AccountCreate(BaseModel):
    name: str
    type: str
    balance: float = 0.0


class AccountRead(BaseModel):
    id: int
    name: str
    type: str
    balance: float

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    account_id: int
    amount: float
    description: str = ""
    type: str


class TransactionRead(BaseModel):
    id: int
    account_id: int
    amount: float
    description: str
    timestamp: datetime
    type: str

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str
    type: str


class CategoryRead(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        from_attributes = True
