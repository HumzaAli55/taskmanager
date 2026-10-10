from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.config import settings
from app.database import engine
from app.routers import auth, tasks

app = FastAPI(title= "Task Manager", debug= settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def root() -> dict:
    return {"status": "ok", "app": "Task Manager"}

