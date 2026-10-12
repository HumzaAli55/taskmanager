from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import User, Task
from app.schemas import TaskResponse, CreateTask, UpdateTask
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("")
def get_tasks(current_user: User = Depends(get_current_user),
              session: Session = Depends(get_session), 
              ) -> list[TaskResponse]:
    return session.exec(select(Task).where(Task.user_id == current_user.id)).all()


@router.post("", status_code=201)
def create_task(
    data: CreateTask,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> TaskResponse :
    task = Task(user_id=current_user.id, **data.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/{task_id}")
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> TaskResponse:
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task 

@router.patch("/(task_id)")
def update_task(
    task_id: int,
    data: UpdateTask,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    session.commit()
    session.refresh(task)
    return task

