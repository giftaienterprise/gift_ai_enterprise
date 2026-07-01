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



    def get_gift_or_none(
        self,
        db: Session,
        gift_id: int,
    ):
        return gift_service.get(
            db,
            gift_id,
        )

    def get_next_image_sort(
        self,
        db: Session,
        gift_id: int,
    ) -> int:
        image = (
            db.query(GiftImage)
            .filter(GiftImage.gift_id == gift_id)
            .order_by(GiftImage.sort.desc())
            .first()
        )

        if not image:
            return 1

        return image.sort + 1

    def create_image(
        self,
        db: Session,
        gift_id: int,
        image_url: str,
    ):
        """
        创建 Gift 图片
        """

        gift = self.get_gift_or_none(
            db,
            gift_id,
        )

        if not gift:
            return None

        first_image = len(gift.images) == 0

        image = gift_image_service.create(
            db,
            GiftImageCreate(
                gift_id=gift_id,
                image_url=image_url,
                sort=self.get_next_image_sort(
                    db,
                    gift_id,
                ),
                is_cover=first_image,
            ),
        )

        if first_image:
            gift.cover = image.image_url
            db.commit()
            db.refresh(gift)

        return image

    def delete_image_file(self, image_url: str):
        """
        删除图片文件（通过 StorageFactory）
        """
        storage = self.get_storage()
        return storage.delete(image_url)

    def delete_image(
            self,
            db: Session,
            image_id: int,
    ):
        """
        企业级删除图片流程：
        1. 查图片
        2. 删除文件（Storage）
        3. 删除数据库记录
        4. 如果是封面，自动重置 cover
        """

        image = gift_image_service.get(db, image_id)

        if not image:
            return False

        gift = image.gift

        storage = self.get_storage()

        # 1. 删除文件
        storage.delete(image.image_url)

        # 2. 判断是否是封面
        is_cover = image.is_cover

        # 3. 删除数据库记录
        gift_image_service.remove(db, image_id)

        # 4. 如果删的是封面，重新设置 cover
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

    def enrich_gift_with_ai(
            self,
            gift_name: str,
            category_name: str | None = None,
            brand_name: str | None = None,
    ):
        """
        AI增强礼品信息（预留能力）
        """

        description = gift_ai_service.generate_description(
            gift_name=gift_name,
            category_name=category_name,
            brand_name=brand_name,
        )

        tags = gift_ai_service.generate_tags(
            gift_name=gift_name,
        )

        return {
            "description": description,
            "tags": tags,
        }

    def create_gift(self, db, data):
        """
        企业级创建礼品（事务版）
        """

        with transaction(db):
            gift = gift_service.create(db, data)

            # 未来扩展：
            # 1. AI生成描述
            # 2. AI生成标签
            # 3. 初始化默认图片
            # 4. 写日志

            return gift

        return gift

gift_business_service = GiftBusinessService()