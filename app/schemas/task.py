from datetime import datetime
from pydantic import BaseModel
from app.models.task import Status


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: Status | None = None
    priority: int | None = 0
    # client may omit due_at; leave it server-controlled if you want
    # You can later add: due_at: datetime | None = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: Status
    priority: int
    due_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
