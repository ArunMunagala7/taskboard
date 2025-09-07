from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/")
def root():
    return {"message": "Taskboard backend is up"}
