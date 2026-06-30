from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.database.session import get_db
from app.schemas.user import UserLogin, UserRegister, UserResponse
from app.services.user_service import authenticate_user, create_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    try:
        user = create_user(db, data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.username, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    token = create_access_token(str(user.id))

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user),
    }