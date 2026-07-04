from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.response import success
from app.core.dependencies import require_admin
from app.database.session import get_db
from app.schemas.brand import BrandCreate, BrandResponse, BrandUpdate
from app.services.crud.brand_service import brand_service


router = APIRouter(prefix="/brands", tags=["brands"])


@router.get("/")
def list_brands(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
):
    result = brand_service.paginate(db, page=page, size=size)

    result["items"] = [
        BrandResponse.model_validate(item).model_dump()
        for item in result["items"]
    ]

    return success(result)


@router.post("/", response_model=BrandResponse, dependencies=[Depends(require_admin)])
def create(data: BrandCreate, db: Session = Depends(get_db)):
    return brand_service.create(db, data)


@router.put("/{brand_id}", response_model=BrandResponse, dependencies=[Depends(require_admin)])
def update(brand_id: int, data: BrandUpdate, db: Session = Depends(get_db)):
    brand = brand_service.get(db, brand_id)

    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")

    return brand_service.update(db, brand, data)


@router.delete("/{brand_id}", dependencies=[Depends(require_admin)])
def delete(brand_id: int, db: Session = Depends(get_db)):
    brand = brand_service.get(db, brand_id)

    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")

    brand_service.remove(db, brand_id)

    return success(message="删除成功")
