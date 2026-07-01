from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success
from app.database.session import get_db
from app.services.business.gift_business_service import gift_business_service


router = APIRouter(
    prefix="/gift-images",
    tags=["gift-image"],
)


@router.delete("/{image_id}")
def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
):
    result = gift_business_service.delete_image(
        db=db,
        image_id=image_id,
    )

    if not result:
        return success(
            message="图片不存在或已删除",
        )

    return success(
        message="删除成功",
    )