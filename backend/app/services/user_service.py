from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserRegister


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, data: UserRegister) -> User:
    existing_user = get_user_by_username(db, data.username)
    if existing_user:
        raise ValueError("用户名已存在")

    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        nickname=data.nickname,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user