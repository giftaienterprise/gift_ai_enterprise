from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.core.response import success
from app.database.session import get_db
from app.models.brand import Brand
from app.models.category import Category
from app.models.gift import Gift
from app.schemas.gift import GiftResponse


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/summary", dependencies=[Depends(require_admin)])
def admin_summary(db: Session = Depends(get_db)):
    recent_gifts = (
        db.query(Gift)
        .order_by(Gift.id.desc())
        .limit(5)
        .all()
    )
    return success(
        {
            "gift_count": db.query(Gift).count(),
            "active_gift_count": db.query(Gift).filter(Gift.is_active.is_(True)).count(),
            "category_count": db.query(Category).count(),
            "brand_count": db.query(Brand).count(),
            "recent_gifts": [
                GiftResponse.model_validate(gift).model_dump()
                for gift in recent_gifts
            ],
        }
    )
