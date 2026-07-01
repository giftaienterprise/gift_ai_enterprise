from contextlib import contextmanager
from sqlalchemy.orm import Session


@contextmanager
def transaction(db: Session):
    """
    统一事务管理。

    用法：

    with transaction(db):
        ...
    """
    try:
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise