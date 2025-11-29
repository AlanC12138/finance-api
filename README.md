![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/python-3.11-blue.svg?style=for-the-badge&logo=python)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge)

# **Personal Finance Manager API**

A production-style backend for personal finance management.
Built with **FastAPI**, **SQLModel**, **JWT auth**, **Argon2 password hashing**, and a clean architecture.

Includes authentication, CRUD models, relational data, transactions, summaries, analytics, and API design.

---

## **Features**

### **Authentication & Security**

* JWT-based authentication
* Argon2 password hashing 
* User-scoped data separation
* Token-protected endpoints

### **Accounts**

* Create checking/savings/cash/credit accounts
* Automatic balance tracking
* User-isolated accounts
* CRUD operations

### **Transactions**

* Income, expense, and transfer support
* Automatic balance updates
* Timestamped entries
* Optional descriptions
* User-scoped isolation

### **Categories**

* Custom user categories
* Income/expense type
* CRUD support
* Ready for transaction linking

### **Summary & Analytics**

* Monthly income/expense totals
* Net cashflow
* Simple category breakdown
* Recent transactions feed
* Account balance overview

---

## **Tech Stack**

* **FastAPI** – high-performance Python backend
* **SQLModel** – modern ORM combining Pydantic + SQLAlchemy
* **SQLite** – simple and portable relational database
* **Argon2 (Passlib)** – secure password hashing
* **PyJWT (python-jose)** – token creation and validation
* **Uvicorn** – ASGI server

---

## **Project Structure**

```
src/finance_api/
│
├── main.py                # App entrypoint + router registration
├── auth.py                # JWT + password hashing + user extraction
├── config.py              # Settings
├── db.py                  # DB engine + session
│
├── models.py              # SQLModel ORM models
├── schemas.py             # Pydantic schemas
│
└── routers/
    ├── auth.py            # Login + register
    ├── accounts.py        # Accounts CRUD
    ├── transactions.py    # Transactions CRUD
    ├── categories.py      # Categories CRUD
    └── summary.py         # Analytics endpoints
```

---

## **Running locally**

### **1. Install dependencies**

```
pip install -r requirements.txt
```

### **2. Start development server**

```
uvicorn src.finance_api.main:app --reload
```

### **3. Open API documentation**

Visit:

```
http://127.0.0.1:8000/docs
```

This includes:

* Interactive testing
* Auth flow (Bearer token)
* All CRUD routes
* Summary endpoints

---

## **Authentication**

### **1. Register**

```
POST /auth/register
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### **2. Login**

```
POST /auth/login
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

Response:

```
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### **3. Authorize**

Click **Authorize** in Swagger and enter:

```
Bearer <your-token>
```

---

## **Example Workflows**

### **Create an account**

```
POST /accounts/
```

### **Add transactions**

```
POST /transactions/
```

### **View monthly summary**

```
GET /summary/monthly?year=2025&month=2
```

### **Recent transactions**

```
GET /summary/recent
```

---

## **Future Enhancements**

* Link transactions → categories
* Budget module (per category or per month)
* Recurring transactions
* Export CSV
* Pagination and filtering
* Graph-ready time series endpoints
* Docker deployment



