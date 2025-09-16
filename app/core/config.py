import os
from pydantic import BaseModel

class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "dev")
    secret_key: str = os.getenv("SECRET_KEY", "change_me")

    db_url: str = (
        f"postgresql+psycopg://{os.getenv('POSTGRES_USER','taskuser')}:"
        f"{os.getenv('POSTGRES_PASSWORD','taskpass')}@{os.getenv('POSTGRES_HOST','localhost')}:"
        f"{os.getenv('POSTGRES_PORT','5432')}/{os.getenv('POSTGRES_DB','taskdb')}"
    )

    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

settings = Settings()
