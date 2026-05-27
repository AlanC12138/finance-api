# finance_api

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?style=flat&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat&logo=docker&logoColor=white)

REST API for personal finance management — track accounts, transactions, and categories with JWT-authenticated endpoints and per-user data isolation.

---

## Quick Start

### Docker (recommended)

```bash
docker build -t finance-api:latest .

docker run --rm -p 8000:8000 \
  -e SECRET_KEY=your-secret-key-here \
  finance-api:latest
```

The SQLite database is created automatically on startup. Visit `http://localhost:8000/docs` for the interactive API docs.

### Local (no Docker)

```bash
pip install -r requirements.txt
uvicorn src.finance_api.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## API Reference

All endpoints except `/health`, `/auth/register`, and `/auth/login` require a Bearer token in the `Authorization` header.

### Auth

| Method | Endpoint          | Description              |
|--------|-------------------|--------------------------|
| POST   | `/auth/register`  | Create a new user        |
| POST   | `/auth/login`     | Log in, get a JWT token  |

**Register / Login request body:**
```json
{ "email": "user@example.com", "password": "yourpassword" }
```

**Login response:**
```json
{ "access_token": "<jwt>", "token_type": "bearer" }
```

### Accounts

| Method | Endpoint          | Description              |
|--------|-------------------|--------------------------|
| POST   | `/accounts/`      | Create an account        |
| GET    | `/accounts/`      | List your accounts       |
| DELETE | `/accounts/{id}`  | Delete an account        |

### Transactions

| Method | Endpoint               | Description                   |
|--------|------------------------|-------------------------------|
| POST   | `/transactions/`       | Record a transaction          |
| GET    | `/transactions/`       | List all transactions         |
| GET    | `/transactions/{id}`   | Get a single transaction      |
| DELETE | `/transactions/{id}`   | Delete a transaction          |

### Categories

| Method | Endpoint              | Description              |
|--------|-----------------------|--------------------------|
| POST   | `/categories/`        | Create a category        |
| GET    | `/categories/`        | List your categories     |
| DELETE | `/categories/{id}`    | Delete a category        |

### Summary

| Method | Endpoint    | Description                              |
|--------|-------------|------------------------------------------|
| GET    | `/summary/` | Monthly income/expense summary per account |

---

## Configuration

| Variable     | Default        | Description                        |
|--------------|----------------|------------------------------------|
| `SECRET_KEY` | `dev-secret`   | JWT signing key — **change this**  |

Copy `.env.example` to `.env` and set your own `SECRET_KEY` before running.

---

## Project Structure

```
finance_api/
├── src/finance_api/
│   ├── main.py          # FastAPI app, lifespan, router registration
│   ├── auth.py          # JWT creation/verification, password hashing
│   ├── config.py        # Settings loaded from environment
│   ├── db.py            # SQLite engine and session dependency
│   ├── models.py        # SQLModel table definitions
│   ├── schemas.py       # Pydantic request/response schemas
│   └── routers/
│       ├── auth.py
│       ├── accounts.py
│       ├── transactions.py
│       ├── categories.py
│       └── summary.py
├── requirements.txt
├── Dockerfile
└── .env.example
```

---

## License

MIT
