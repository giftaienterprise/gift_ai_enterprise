from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.core.response import success
from app.database.session import get_db
from app.schemas.site_setting import (
    SiteSettingPublic,
    SiteSettingResponse,
    SiteSettingUpdate,
)
from app.services.site_setting_service import site_setting_service


router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/public")
def get_public_settings(db: Session = Depends(get_db)):
    settings = site_setting_service.get_or_create(db)
    return success(
        SiteSettingPublic.model_validate(settings).model_dump()
    )


@router.get("/", dependencies=[Depends(require_admin)])
def get_settings(db: Session = Depends(get_db)):
    settings = site_setting_service.get_or_create(db)
    return success(
        SiteSettingResponse.model_validate(settings).model_dump()
    )


@router.put("/", dependencies=[Depends(require_admin)])
def update_settings(
    data: SiteSettingUpdate,
    db: Session = Depends(get_db),
):
    settings = site_setting_service.update(db, data)
    return success(
        SiteSettingResponse.model_validate(settings).model_dump()
    )
