from pydantic import BaseModel


class SiteSettingPublic(BaseModel):
    wechat_id: str
    wechat_qr_url: str
    phone: str
    share_title: str
    share_description: str
    share_image_url: str

    model_config = {"from_attributes": True}


class SiteSettingResponse(SiteSettingPublic):
    id: int

    model_config = {"from_attributes": True}


class SiteSettingUpdate(BaseModel):
    wechat_id: str | None = None
    wechat_qr_url: str | None = None
    phone: str | None = None
    share_title: str | None = None
    share_description: str | None = None
    share_image_url: str | None = None
