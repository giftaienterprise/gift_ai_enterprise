from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.response import success
from app.database.session import get_db
from app.schemas.gift import GiftCreate, GiftResponse, GiftUpdate
from app.schemas.gift_image import GiftImageResponse

from app.core.dependencies import get_current_user, get_gift_business_service
from app.services.crud.gift_service import gift_service


router = APIRouter(
    prefix="/gifts",
    tags=["gifts"],
)


class GiftImageAttachRequest(BaseModel):
    image_url: str


# =========================
# Gift List
# =========================
@router.get("/")
def list_gifts(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
):
    result = gift_service.paginate_with_relations(
        db,
        page=page,
        size=size,
    )

    result["items"] = [
        GiftResponse.model_validate(item).model_dump()
        for item in result["items"]
    ]

    return success(result)


# =========================
# Gift Detail
# =========================
@router.get("/{gift_id}")
def get_gift(
    gift_id: int,
    db: Session = Depends(get_db),
):
    gift = gift_service.get_with_relations(
        db,
        gift_id,
    )

    if not gift:
        raise HTTPException(
            status_code=404,
            detail="礼品不存在",
        )

    return success(
        GiftResponse.model_validate(gift).model_dump()
    )


# =========================
# Create Gift (DI + Business)
# =========================
@router.post("/", response_model=GiftResponse, dependencies=[Depends(get_current_user)])
def create(
    data: GiftCreate,
    db: Session = Depends(get_db),
    gift_business=Depends(get_gift_business_service),
):
    return gift_business.create_gift(
        db=db,
        data=data,
    )


# =========================
# Attach Image (DI + Business)
# =========================
@router.post("/{gift_id}/images", dependencies=[Depends(get_current_user)])
def attach_gift_image(
    gift_id: int,
    data: GiftImageAttachRequest,
    db: Session = Depends(get_db),
    gift_business=Depends(get_gift_business_service),
):
    image = gift_business.create_image(
        db=db,
        gift_id=gift_id,
        image_url=data.image_url,
    )

    if not image:
        raise HTTPException(
            status_code=404,
            detail="礼品不存在",
        )

    return success(
        GiftImageResponse.model_validate(image).model_dump()
    )


# =========================
# Update Gift
# =========================
@router.put("/{gift_id}", response_model=GiftResponse, dependencies=[Depends(get_current_user)])
def update(
    gift_id: int,
    data: GiftUpdate,
    db: Session = Depends(get_db),
):
    gift = gift_service.get(
        db,
        gift_id,
    )

    if not gift:
        raise HTTPException(
            status_code=404,
            detail="礼品不存在",
        )

    return gift_service.update(
        db,
        gift,
        data,
    )


# =========================
# Delete Gift
# =========================
@router.delete("/{gift_id}", dependencies=[Depends(get_current_user)])
def delete(
    gift_id: int,
    db: Session = Depends(get_db),
):
    gift = gift_service.get(
        db,
        gift_id,
    )

    if not gift:
        raise HTTPException(
            status_code=404,
            detail="礼品不存在",
        )

    gift_service.remove(
        db,
        gift_id,
    )

    return success(
        message="删除成功",
    )
