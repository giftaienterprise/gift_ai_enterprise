from pydantic import BaseModel


class BrandCreate(BaseModel):
    name: str
    logo: str | None = None
    website: str | None = None
    description: str | None = None
    sort: int = 0
    is_active: bool = True


class BrandUpdate(BaseModel):
    name: str | None = None
    logo: str | None = None
    website: str | None = None
    description: str | None = None
    sort: int | None = None
    is_active: bool | None = None


class BrandResponse(BaseModel):
    id: int
    name: str
    logo: str | None = None
    website: str | None = None
    description: str | None = None
    sort: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }