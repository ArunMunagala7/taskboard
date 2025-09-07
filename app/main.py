from fastapi import FastAPI
from app.api.routes import api_router

app = FastAPI(title="Taskboard API", version="0.1.0")

@app.get("/admin/health")
def health():
    return {"status": "ok"}

app.include_router(api_router)
