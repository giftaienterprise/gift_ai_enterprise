from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class GiftImage(Base):
    __tablename__ = "gift_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    gift_id: Mapped[int] = mapped_column(
        ForeignKey("gifts.id", ondelete="CASCADE"),
        nullable=False,
    )

    image_url: Mapped[str] = mapped_column(String(500), nullable=False)

    sort: Mapped[int] = mapped_column(Integer, default=0)

    is_cover: Mapped[bool] = mapped_column(Boolean, default=False)

    gift = relationship(
        "Gift",
        back_populates="images",
    )