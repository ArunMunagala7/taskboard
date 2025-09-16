import os
from pydantic import BaseModel

class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "dev")
    secret_key: str = os.getenv("SECRET_KEY", "change_me")

    # If running inside GitHub Actions, use localhost
    db_host: str = "localhost" if os.getenv("GITHUB_ACTIONS") else os.getenv("POSTGRES_HOST", "db")

    db_url: str = (
        f"postgresql+psycopg://{os.getenv('POSTGRES_USER','taskuser')}:"
        f"{os.getenv('POSTGRES_PASSWORD','taskpass')}@{db_host}:"
        f"{os.getenv('POSTGRES_PORT','5432')}/{os.getenv('POSTGRES_DB','taskdb')}"
    )

settings = Settings()
