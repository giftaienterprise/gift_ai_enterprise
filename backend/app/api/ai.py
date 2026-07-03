from pydantic import BaseModel
from fastapi import APIRouter, Depends

from app.core.dependencies import enforce_ai_rate_limit
from app.services.business.ai_business_service import ai_business_service


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
    dependencies=[Depends(enforce_ai_rate_limit)],
)


# =========================
# Request Models
# =========================

class ProductDescriptionRequest(BaseModel):
    name: str
    category_name: str | None = None
    brand_name: str | None = None
    price: float | None = None


class ProductTagsRequest(ProductDescriptionRequest):
    description: str | None = None


class ImageRecognitionRequest(BaseModel):
    image_url: str


class AnalyzeProductRequest(ProductTagsRequest):
    image_url: str | None = None


# =========================
# Response Helper
# =========================

def response(message: str, result):
    return {
        "success": getattr(result, "success", True),
        "message": message,
        "data": getattr(result, "data", None),
        "error": getattr(result, "error", None),
    }


# =========================
# API
# =========================

@router.get("/test")
async def test_ai():
    result = await ai_business_service.test_connection()
    return response("DeepSeek connected", result)


@router.post("/product-description")
async def product_description(data: ProductDescriptionRequest):

    result = await ai_business_service.generate_product_description(
        name=data.name,
        category_name=data.category_name,
        brand_name=data.brand_name,
        price=data.price,
    )

    return response("AI 商品描述生成成功", result)


@router.post("/product-tags")
async def product_tags(data: ProductTagsRequest):

    result = await ai_business_service.generate_product_tags(
        name=data.name,
        category_name=data.category_name,
        brand_name=data.brand_name,
        description=data.description,
        price=data.price,
    )

    return response("AI 商品标签生成成功", result)


@router.post("/image-recognition")
async def image_recognition(data: ImageRecognitionRequest):

    result = await ai_business_service.recognize_image(
        image_url=data.image_url
    )

    return response("AI 图片识别完成", result)


@router.post("/analyze-product")
async def analyze_product(data: AnalyzeProductRequest):

    result = await ai_business_service.analyze_product(
        name=data.name,
        category_name=data.category_name,
        brand_name=data.brand_name,
        description=data.description,
        price=data.price,
        image_url=data.image_url,
    )

    return response("AI 商品统一分析成功", result)
