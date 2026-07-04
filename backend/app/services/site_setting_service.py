from sqlalchemy.orm import Session

from app.models.site_setting import SiteSetting
from app.schemas.site_setting import SiteSettingUpdate


DEFAULTS = {
    "wechat_id": "",
    "wechat_qr_url": "",
    "phone": "",
    "share_title": "AI送礼参谋",
    "share_description": "发现更贴心的礼物",
    "share_image_url": "",
}


class SiteSettingService:
    def get_or_create(self, db: Session) -> SiteSetting:
        settings = db.get(SiteSetting, 1)
        if settings is None:
            settings = SiteSetting(id=1, **DEFAULTS)
            db.add(settings)
            db.commit()
            db.refresh(settings)
        return settings

    def update(self, db: Session, data: SiteSettingUpdate) -> SiteSetting:
        settings = self.get_or_create(db)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(settings, field, value)
        db.commit()
        db.refresh(settings)
        return settings


site_setting_service = SiteSettingService()
