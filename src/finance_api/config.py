from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret"
    ALGORITHM: str = "HS256"

settings = Settings()