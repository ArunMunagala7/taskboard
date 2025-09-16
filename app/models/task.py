import enum
from datetime import datetime

from sqlalchemy import (
    String,
    ForeignKey,
    Enum as SAEnum,
    Integer,
    TIMESTAMP,
    DateTime,
    func,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Status(str, enum.Enum):
    todo = "todo"
    doing = "doing"
    done = "done"


class Task(Base):
    __tablename__ = "tasks"

    # helpful composite index for common listing pattern
    __table_args__ = (
        Index("ix_tasks_project_created_at", "project_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)

    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None]
    status: Mapped[Status] = mapped_column(SAEnum(Status), default=Status.todo)
    priority: Mapped[int] = mapped_column(Integer, default=0)

    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), default=None)

    # optional due date
    due_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=False), default=None)

    # NEW: timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    project = relationship("Project")
