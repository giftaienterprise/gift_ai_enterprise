from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    icon: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    sort: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )