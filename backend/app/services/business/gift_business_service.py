from sqlalchemy.orm import Session

from app.models.gift_image import GiftImage
from app.schemas.gift_image import GiftImageCreate
from app.services.crud.gift_service import gift_service
from app.services.crud.gift_image_service import gift_image_service
from app.services.business.base import BaseBusinessService
from app.services.ai.gift_ai_service import gift_ai_service
from app.core.transaction import transaction


class GiftBusinessService(BaseBusinessService):
    """
    Gift 企业级业务服务层
    """

    def get_gift_or_none(self, db: Session, gift_id: int):
        return gift_service.get(db, gift_id)

    def get_next_image_sort(self, db: Session, gift_id: int) -> int:
        image = (
            db.query(GiftImage)
            .filter(GiftImage.gift_id == gift_id)
            .order_by(GiftImage.sort.desc())
            .first()
        )

        if not image:
            return 1

        return image.sort + 1

    def create_image(self, db: Session, gift_id: int, image_url: str):
        gift = self.get_gift_or_none(db, gift_id)

        if not gift:
            return None

        first_image = len(gift.images) == 0

        image = gift_image_service.create(
            db,
            GiftImageCreate(
                gift_id=gift_id,
                image_url=image_url,
                sort=self.get_next_image_sort(db, gift_id),
                is_cover=first_image,
            ),
        )

        if first_image:
            gift.cover = image.image_url
            db.commit()
            db.refresh(gift)

        return image

    def delete_image_file(self, image_url: str):
        storage = self.get_storage()
        return storage.delete(image_url)

    def delete_image(self, db: Session, image_id: int):
        image = gift_image_service.get(db, image_id)

        if not image:
            return False

        gift = image.gift
        storage = self.get_storage()

        storage.delete(image.image_url)

        is_cover = image.is_cover

        gift_image_service.remove(db, image_id)

        if is_cover:
            next_image = (
                db.query(GiftImage)
                .filter(GiftImage.gift_id == gift.id)
                .order_by(GiftImage.sort.asc())
                .first()
            )

            if next_image:
                gift.cover = next_image.image_url
            else:
                gift.cover = None

            db.commit()
            db.refresh(gift)

        return True

    def create_gift(self, db, data):
        with transaction(db):
            gift = gift_service.create(db, data)
            return gift

    def generate_ai_description(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        price: float | None = None,
    ) -> dict:
        return gift_ai_service.generate_product_description(
            name=name,
            category_name=category_name,
            brand_name=brand_name,
            price=price,
        )

    def generate_ai_tags(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        description: str | None = None,
        price: float | None = None,
    ) -> dict:
        return gift_ai_service.generate_product_tags(
            name=name,
            category_name=category_name,
            brand_name=brand_name,
            description=description,
            price=price,
        )

    def recognize_ai_image(self, image_url: str) -> dict:
        return gift_ai_service.recognize_product_image(
            image_url=image_url,
        )

    async def analyze_ai_product(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        description: str | None = None,
        price: float | None = None,
        image_url: str | None = None,
    ) -> dict:
        """
        🚀 并行 AI 商品分析
        """

        return await gift_ai_service.analyze_product_parallel(
            name=name,
            category_name=category_name,
            brand_name=brand_name,
            description=description,
            price=price,
            image_url=image_url,
        )


gift_business_service = GiftBusinessService()