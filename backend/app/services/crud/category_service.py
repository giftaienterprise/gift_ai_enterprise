from app.core.crud import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


category_service = CRUDBase[
    Category,
    CategoryCreate,
    CategoryUpdate,
](Category)