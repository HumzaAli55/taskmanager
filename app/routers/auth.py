from fastapi import APIRouter , HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.database import get_session
from app.models import User
from app.schemas import RegisterRequest, LoginResponse, UserResponse
from app.auth import hash_password, verify_password, create_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201)
def register(data: RegisterRequest, session:Session = Depends(get_session)) -> UserResponse:
    existing = session.exec(select(User).where(User.username == data.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    user = User(username=data.username, hashed_password= hash_password(data.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(get_session)) ->  LoginResponse:
    user = session.exec(select(User).where(User.username == form.username)).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token(user.id, user.username)
    return LoginResponse(access_token=token)

@router.get("/me")
def me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return current_user
    