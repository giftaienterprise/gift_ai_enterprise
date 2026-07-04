from fastapi import APIRouter

from app.core.response import success
from app.schemas.advisor import RecommendRequest
from app.services.ai.gift_recommendation_service import gift_recommendation_service


router = APIRouter(prefix="/advisor", tags=["advisor"])


@router.post("/recommend")
def recommend_gifts(data: RecommendRequest):
    result = gift_recommendation_service.recommend(data)
    return success(result.model_dump())
