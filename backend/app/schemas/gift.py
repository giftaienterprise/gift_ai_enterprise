from typing import List

from pydantic import BaseModel

from app.schemas.brand import BrandResponse
from app.schemas.category import CategoryResponse
from app.schemas.gift_image import GiftImageResponse


class GiftCreate(BaseModel):
    name: str
    subtitle: str = ""
    category_id: int
    brand_id: int
    price: int = 0
    cover: str = ""
    description: str = ""
    is_active: bool = True
    sort: int = 0


class GiftUpdate(BaseModel):
    name: str | None = None
    subtitle: str | None = None
    category_id: int | None = None
    brand_id: int | None = None
    price: int | None = None
    cover: str | None = None
    description: str | None = None
    is_active: bool | None = None
    sort: int | None = None


class GiftResponse(BaseModel):
    id: int
    name: str
    subtitle: str
    category_id: int
    brand_id: int
    price: int
    cover: str
    description: str
    is_active: bool
    sort: int

    category: CategoryResponse | None = None
    brand: BrandResponse | None = None
    images: List[GiftImageResponse] = []

    model_config = {
        "from_attributes": True
    }