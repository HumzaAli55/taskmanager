from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    hashed_password: str


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title:str
    description:str = ""
    completed:bool = False
    created_at:datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")


