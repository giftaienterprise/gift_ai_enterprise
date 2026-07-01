from app.services.ai.context.product_context import ProductContext


class ProductContextBuilder:

    def build(
        self,
        name: str,
        category: str | None = None,
        brand: str | None = None,
        price: float | None = None,
        description: str | None = None,
        image_url: str | None = None,
    ) -> ProductContext:

        return ProductContext(
            name=name,
            category=category,
            brand=brand,
            price=price,
            description=description,
            image_url=image_url,
        )


product_context_builder = ProductContextBuilder()