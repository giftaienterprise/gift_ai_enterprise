from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.auth import router as auth_router
from app.api.category import router as category_router
from app.api.brand import router as brand_router
from app.core.config import settings
from app.core.exceptions import (
    BusinessException,
    business_exception_handler,
    validation_exception_handler,
)
from app.api.gift import router as gift_router
from fastapi.staticfiles import StaticFiles
from app.api.upload import router as upload_router
from app.api.gift_image import router as gift_image_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.mount(
    settings.UPLOAD_URL_PREFIX,
    StaticFiles(directory=settings.UPLOAD_DIR),
    name="uploads",
)

# 注册异常处理
app.add_exception_handler(
    BusinessException,
    business_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

# 注册 API 路由
app.include_router(auth_router, prefix="/api")
app.include_router(category_router, prefix="/api")
app.include_router(brand_router, prefix="/api")
app.include_router(gift_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
app.include_router(gift_image_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Gift AI Enterprise API",
        "version": settings.APP_VERSION,
    }