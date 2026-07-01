from app.database.session import Base, engine

# 导入所有模型，确保 SQLAlchemy 注册
from app.models import User, Category, Brand, Gift


def init_db():
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成")


if __name__ == "__main__":
    init_db()