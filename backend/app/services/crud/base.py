from sqlalchemy.orm import Session


class BaseCRUDService:
    """
    企业级通用 CRUD 基类

    统一封装：
    - get
    - list
    - create
    - update
    - delete
    """

    model = None

    def get(self, db: Session, obj_id: int):
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def list(self, db: Session, skip: int = 0, limit: int = 20):
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj):
        db.delete(obj)
        db.commit()
        return True