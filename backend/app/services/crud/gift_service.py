from sqlalchemy.orm import Session, joinedload

from app.core.crud import CRUDBase
from app.models.gift import Gift
from app.schemas.gift import GiftCreate, GiftUpdate


class GiftService(CRUDBase[Gift, GiftCreate, GiftUpdate]):

    def paginate_with_relations(
        self,
        db: Session,
        page: int = 1,
        size: int = 10,
    ):
        query = (
            db.query(Gift)
            .options(
                joinedload(Gift.category),
                joinedload(Gift.brand),
                joinedload(Gift.images),
            )
        )

        total = query.count()

        items = (
            query
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )

        return {
            "total": total,
            "page": page,
            "size": size,
            "items": items,
        }

    def get_with_relations(
        self,
        db: Session,
        gift_id: int,
    ):
        return (
            db.query(Gift)
            .options(
                joinedload(Gift.category),
                joinedload(Gift.brand),
                joinedload(Gift.images),
            )
            .filter(Gift.id == gift_id)
            .first()
        )


gift_service = GiftService(Gift)