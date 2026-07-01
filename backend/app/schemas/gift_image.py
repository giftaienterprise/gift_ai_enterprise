from pydantic import BaseModel


class GiftImageCreate(BaseModel):
    gift_id: int
    image_url: str
    sort: int = 0
    is_cover: bool = False


class GiftImageUpdate(BaseModel):
    image_url: str | None = None
    sort: int | None = None
    is_cover: bool | None = None


class GiftImageResponse(BaseModel):
    id: int
    gift_id: int
    image_url: str
    sort: int
    is_cover: bool

    model_config = {
        "from_attributes": True
    }


class GiftImageSortItem(BaseModel):
    id: int
    sort: int


class GiftImageSortRequest(BaseModel):
    items: list[GiftImageSortItem]