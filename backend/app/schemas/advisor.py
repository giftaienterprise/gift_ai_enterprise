from pydantic import BaseModel, Field


class RecommendRequest(BaseModel):
    relation: str = Field(min_length=1, max_length=50)
    scene: str = Field(min_length=1, max_length=50)
    budget: str = Field(min_length=1, max_length=50)
    note: str = ""
    platform: str = "taobao"


class RecommendedGift(BaseModel):
    id: str
    name: str
    price: int
    emoji: str = "🎁"
    reason: str = ""
    match: str = ""
    meaning: str = ""
    tip: str = ""
    tags: list[str] = []
    purchase_url: str
    platform: str
    platform_links: dict[str, str] = {}


class RecommendResponse(BaseModel):
    success: bool
    combo_title: str = ""
    relation: str
    scene: str
    budget: str
    gifts: list[RecommendedGift] = []
    source: str = "deepseek"
    error: str | None = None
