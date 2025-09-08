from sqlalchemy import String, ForeignKey, Enum, Integer, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base
import enum
from datetime import datetime  # ✅ add this


class Status(str, enum.Enum):
    todo = "todo"
    doing = "doing"
    done = "done"

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None]
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.todo)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), default=None)
    due_at: Mapped["datetime | None"] = mapped_column(TIMESTAMP(timezone=False), default=None)

    project = relationship("Project")
