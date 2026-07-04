from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

# =========================
# Core Config
# =========================
from app.core.config import settings

# =========================
# Exception Handler
# =========================
from app.core.exceptions import (
    BusinessException,
    business_exception_handler,
    validation_exception_handler,
)

# =========================
# Routers
# =========================
from app.api.ai import router as ai_router
from app.api.agent import router as agent_router
from app.api.auth import router as auth_router
from app.api.brand import router as brand_router
from app.api.category import router as category_router
from app.api.gift import router as gift_router
from app.api.gift_image import router as gift_image_router
from app.api.upload import router as upload_router
from app.api.admin import router as admin_router
from app.api.site_setting import router as site_setting_router

# =========================
# App Init
# =========================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


# =========================
# Static Files（上传文件）
# =========================
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
app.mount(
    settings.UPLOAD_URL_PREFIX,
    StaticFiles(directory=settings.UPLOAD_DIR),
    name="uploads",
)


# =========================
# Exception Handlers
# =========================
app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# =========================
# Register Routers
# =========================
app.include_router(ai_router)
app.include_router(agent_router)
app.include_router(auth_router, prefix="/api")
app.include_router(category_router, prefix="/api")
app.include_router(brand_router, prefix="/api")
app.include_router(gift_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
app.include_router(gift_image_router, prefix="/api")
app.include_router(site_setting_router, prefix="/api")
app.include_router(admin_router, prefix="/api")


# =========================
# Root Test
# =========================
@app.get("/")
def root():
    return {
        "message": "Gift AI Enterprise API",
        "version": settings.APP_VERSION,
    }


# =========================
# Health Check
# =========================
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
