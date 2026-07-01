from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.session import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def get(self, db: Session, obj_id: int) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(
        self,
        db: Session,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)

        return db_obj

    def remove(
        self,
        db: Session,
        obj_id: int,
    ) -> ModelType | None:
        obj = self.get(db, obj_id)

        if not obj:
            return None

        db.delete(obj)
        db.commit()

        return obj

    def paginate(
        self,
        db: Session,
        page: int = 1,
        size: int = 10,
    ):
        query = db.query(self.model)

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