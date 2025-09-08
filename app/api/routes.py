from fastapi import APIRouter
from . import projects, tasks, auth

api_router = APIRouter()

@api_router.get("/")
def root():
    return {"message": "Taskboard backend is up"}

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(tasks.router, tags=["tasks"])
