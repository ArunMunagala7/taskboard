import os
from pydantic import BaseModel

class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "dev")

settings = Settings()
