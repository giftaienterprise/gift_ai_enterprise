from pydantic import BaseModel
from typing import List, Optional


class ProductAIResult(BaseModel):
    """
    企业级 AI 商品标准输出结构
    """

    title: str
    subtitle: str
    description: str
    selling_points: List[str]

    confidence: float = 0.0
    model: Optional[str] = None