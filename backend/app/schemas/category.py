from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    icon: str | None = None
    sort: int = 0
    is_active: bool = True


class CategoryUpdate(BaseModel):
    name: str | None = None
    icon: str | None = None
    sort: int | None = None
    is_active: bool | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    icon: str | None = None
    sort: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }