from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectOut
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter()

@router.post("", response_model=ProjectOut)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    proj = Project(owner_id=current_user.id, name=payload.name, description=payload.description)
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj

@router.get("", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # show only user-owned projects (simple version)
    return db.query(Project).filter(Project.owner_id == current_user.id).all()
