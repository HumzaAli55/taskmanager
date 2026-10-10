from pydantic import BaseModel
from datetime import datetime

# ---- Auth ----

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    username: str

#----Tasks-----
class CreateTask(BaseModel):
    title: str
    description: str = ""

class UpdateTask(BaseModel):
    title: str | None = None
    description : str | None = None
    completed : bool | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
    user_id: int