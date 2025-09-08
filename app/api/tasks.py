from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.task import Task, Status
from app.schemas.task import TaskCreate, TaskOut

router = APIRouter()

@router.post("/projects/{project_id}/tasks", response_model=TaskOut)
def create_task(project_id: int, payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        project_id=project_id,
        title=payload.title,
        description=payload.description,
        status=payload.status or Status.todo,
        priority=payload.priority or 0,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/projects/{project_id}/tasks", response_model=list[TaskOut])
def list_tasks(project_id: int, db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.project_id == project_id).all()
