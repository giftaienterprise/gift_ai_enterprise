from app.database.session import Base, engine
from app.models import User


def init_db():
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成")


if __name__ == "__main__":
    init_db()