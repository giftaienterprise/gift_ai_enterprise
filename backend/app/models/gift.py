from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Gift(Base):
    __tablename__ = "gifts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
    )

    subtitle: Mapped[str] = mapped_column(
        String(500),
        default="",
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
    )

    brand_id: Mapped[int] = mapped_column(
        ForeignKey("brands.id"),
    )

    price: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    cover: Mapped[str] = mapped_column(
        String(500),
        default="",
    )

    description: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    sort: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    images = relationship(
        "GiftImage",
        back_populates="gift",
        cascade="all, delete-orphan",
        order_by="GiftImage.sort",
    )
    category = relationship("Category")
    brand = relationship("Brand")