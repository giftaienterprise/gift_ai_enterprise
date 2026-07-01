from pydantic import BaseModel
from fastapi import APIRouter

from app.services.business.ai_business_service import ai_business_service
from app.services.business.gift_business_service import gift_business_service


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


class ProductDescriptionRequest(BaseModel):
    name: str
    category_name: str | None = None
    brand_name: str | None = None
    price: float | None = None


class ProductTagsRequest(BaseModel):
    name: str
    category_name: str | None = None
    brand_name: str | None = None
    description: str | None = None
    price: float | None = None


class ImageRecognitionRequest(BaseModel):
    image_url: str


class AnalyzeProductRequest(BaseModel):
    name: str
    category_name: str | None = None
    brand_name: str | None = None
    description: str | None = None
    price: float | None = None
    image_url: str | None = None


@router.get("/test")
def test_ai():
    result = ai_business_service.test_connection()

    return {
        "success": True,
        "message": "DeepSeek connected.",
        "data": result,
    }


@router.post("/product-description")
def generate_product_description(data: ProductDescriptionRequest):
    result = gift_business_service.generate_ai_description(
        name=data.name,
        category_name=data.category_name,
        brand_name=data.brand_name,
        price=data.price,
    )

    return {
        "success": True,
        "message": "AI 商品描述生成成功",
        "data": result,
    }


@router.post("/product-tags")
def generate_product_tags(data: ProductTagsRequest):
    result = gift_business_service.generate_ai_tags(
        name=data.name,
        category_name=data.category_name,
        brand_name=data.brand_name,
        description=data.description,
        price=data.price,
    )

    return {
        "success": True,
        "message": "AI 商品标签生成成功",
        "data": result,
    }


@router.post("/image-recognition")
def recognize_product_image(data: ImageRecognitionRequest):
    result = gift_business_service.recognize_ai_image(
        image_url=data.image_url,
    )

    return {
        "success": True,
        "message": "AI 图片识别完成",
        "data": result,
    }

@router.post("/analyze-product")
async def analyze_product(data: AnalyzeProductRequest):
    result = await gift_business_service.analyze_ai_product(
        name=data.name,
        category_name=data.category_name,
        brand_name=data.brand_name,
        description=data.description,
        price=data.price,
        image_url=data.image_url,
    )

    return {
        "success": True,
        "message": "AI 商品统一分析成功",
        "data": result,
    }