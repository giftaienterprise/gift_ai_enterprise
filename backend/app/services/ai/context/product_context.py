from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductContext:
    name: str
    category: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    image_url: Optional[str] = None