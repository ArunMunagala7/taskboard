from pydantic import BaseModel
from app.models.task import Status

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: Status | None = None
    priority: int | None = 0

class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: Status
    priority: int
    class Config:
        from_attributes = True
