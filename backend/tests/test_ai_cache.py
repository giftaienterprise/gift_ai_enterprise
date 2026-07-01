import asyncio

from app.services.business.ai_business_service import ai_business_service


async def main():
    result = await ai_business_service.generate_product_description(
        name="智能保温杯",
        category_name="生活用品",
        brand_name="GiftAI",
        price=99.0,
    )

    print("AI Cache Test Result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())