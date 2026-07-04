from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.session import get_db
from app.models.user import User
from app.core.rate_limit import ai_rate_limiter
from app.services.business.gift_business_service import gift_business_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=401,
        detail="INVALID_AUTHENTICATION",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        user_id = int(decode_access_token(token))
    except (JWTError, ValueError) as exc:
        raise credentials_exception() from exc

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise credentials_exception()
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="ADMIN_REQUIRED")
    return current_user


def enforce_ai_rate_limit(
    current_user: User = Depends(get_current_user),
) -> User:
    if not ai_rate_limiter.allow(str(current_user.id)):
        raise HTTPException(status_code=429, detail="AI_RATE_LIMIT_EXCEEDED")
    return current_user


def get_gift_business_service():
    """
    获取 GiftBusinessService 实例
    """
    return gift_business_service
