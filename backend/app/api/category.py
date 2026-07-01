from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.response import success
from app.database.session import get_db
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.crud.category_service import category_service


router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/")
def list_categories(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
):
    result = category_service.paginate(db, page=page, size=size)

    result["items"] = [
        CategoryResponse.model_validate(item).model_dump()
        for item in result["items"]
    ]

    return success(result)


@router.post("/", response_model=CategoryResponse)
def create(data: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create(db, data)


@router.put("/{category_id}", response_model=CategoryResponse)
def update(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    category = category_service.get(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")

    return category_service.update(db, category, data)


@router.delete("/{category_id}")
def delete(category_id: int, db: Session = Depends(get_db)):
    category = category_service.get(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")

    category_service.remove(db, category_id)

    return success(message="删除成功")