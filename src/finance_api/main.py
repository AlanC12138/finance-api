from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routers import auth, categories, transactions, accounts, summary
from .db import engine
from .models import SQLModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    SQLModel.metadata.create_all(engine)
    yield
    # Shutdown logic (if any)


app = FastAPI(
    title="Personal Finance Manager API",
    version="0.1.0",
    lifespan=lifespan
)


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# Register routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(summary.router, prefix="/summary", tags=["summary"])

