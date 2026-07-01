from app.core.crud import CRUDBase
from app.models.brand import Brand
from app.schemas.brand import BrandCreate, BrandUpdate


brand_service = CRUDBase[
    Brand,
    BrandCreate,
    BrandUpdate,
](Brand)