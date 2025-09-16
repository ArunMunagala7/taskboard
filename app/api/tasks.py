from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.deps import get_current_user
from app.core.cache import cache_get, cache_set, cache_delete_pattern
from app.models.task import Task, Status
from app.models.user import User
from app.schemas.task import TaskCreate, TaskOut

router = APIRouter()


def _key_for_list(
    project_id: int,
    status, assignee_id, priority_min, priority_max, due_after, due_before, q,
    order_by, order, page, limit,
) -> str:
    parts = [
        f"p:{project_id}",
        f"s:{status or ''}",
        f"a:{assignee_id or ''}",
        f"pmin:{priority_min}",
        f"pmax:{'' if priority_max is None else priority_max}",
        f"da:{'' if due_after is None else due_after.isoformat()}",
        f"db:{'' if due_before is None else due_before.isoformat()}",
        f"q:{q or ''}",
        f"ob:{order_by}",
        f"o:{order}",
        f"pg:{page}",
        f"lim:{limit}",
    ]
    return "tasks:" + "|".join(parts)


@router.post("/projects/{project_id}/tasks", response_model=TaskOut)
def create_task(
    project_id: int,
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = Task(
        project_id=project_id,
        title=payload.title,
        description=payload.description,
        status=payload.status or Status.todo,
        priority=payload.priority or 0,
        # due_at can be wired in later if you expose it in TaskCreate
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    # invalidate cached lists for this project
    cache_delete_pattern(f"tasks:p:{project_id}*")

    return task


@router.get("/projects/{project_id}/tasks")
def list_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),

    status: Status | None = Query(None),
    assignee_id: int | None = Query(None),
    priority_min: int = Query(0, ge=0),
    priority_max: int | None = Query(None),
    due_after: datetime | None = Query(None),
    due_before: datetime | None = Query(None),
    q: str | None = Query(None),

    # NEW default: latest first
    order_by: Literal["created_at", "due_at", "priority", "id"] = "created_at",
    order: Literal["asc", "desc"] = "desc",
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    key = _key_for_list(project_id, status, assignee_id, priority_min, priority_max,
                        due_after, due_before, q, order_by, order, page, limit)

    cached = cache_get(key)
    if cached is not None:
        return cached  # cache hit

    query = db.query(Task).filter(Task.project_id == project_id)
    if status:
        query = query.filter(Task.status == status)
    if assignee_id is not None:
        query = query.filter(Task.assignee_id == assignee_id)
    if priority_min is not None:
        query = query.filter(Task.priority >= priority_min)
    if priority_max is not None:
        query = query.filter(Task.priority <= priority_max)
    if due_after is not None:
        query = query.filter(Task.due_at != None, Task.due_at >= due_after)  # noqa: E711
    if due_before is not None:
        query = query.filter(Task.due_at != None, Task.due_at <= due_before)  # noqa: E711
    if q:
        query = query.filter(Task.title.ilike(f"%{q}%"))

    total = query.count()
    col = {
        "created_at": Task.created_at,
        "due_at": Task.due_at,
        "priority": Task.priority,
        "id": Task.id,
    }[order_by]
    query = query.order_by(col.asc() if order == "asc" else col.desc())

    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    payload = {
        "items": [TaskOut.model_validate(i).model_dump() for i in items],
        "page": page,
        "limit": limit,
        "total": total,
    }

    cache_set(key, payload, ttl=60)  # 60s TTL
    return payload
