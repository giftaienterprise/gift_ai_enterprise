from sqlalchemy.orm import Session

from app.models.gift_image import GiftImage
from app.schemas.gift_image import GiftImageCreate, GiftImageUpdate
from app.services.crud.base import BaseCRUDService


class GiftImageService(BaseCRUDService):
    """
    GiftImage CRUD 服务
    """

    model = GiftImage

    def create(self, db: Session, data: GiftImageCreate):
        obj = GiftImage(**data.model_dump())

        return super().create(
            db,
            obj,
        )

    def update(self, db: Session, obj: GiftImage, data: GiftImageUpdate):
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)

        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, image_id: int):
        obj = self.get(
            db,
            image_id,
        )

        if not obj:
            return False

        return super().delete(
            db,
            obj,
        )

    def list_by_gift_id(self, db: Session, gift_id: int):
        return (
            db.query(GiftImage)
            .filter(GiftImage.gift_id == gift_id)
            .order_by(GiftImage.sort.asc())
            .all()
        )


gift_image_service = GiftImageService()