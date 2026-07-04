from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SiteSetting(Base):
    __tablename__ = "site_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    wechat_id: Mapped[str] = mapped_column(String(100), default="")
    wechat_qr_url: Mapped[str] = mapped_column(String(500), default="")
    phone: Mapped[str] = mapped_column(String(30), default="")
    share_title: Mapped[str] = mapped_column(String(150), default="AI送礼参谋")
    share_description: Mapped[str] = mapped_column(
        String(500),
        default="发现更贴心的礼物",
    )
    share_image_url: Mapped[str] = mapped_column(String(500), default="")
