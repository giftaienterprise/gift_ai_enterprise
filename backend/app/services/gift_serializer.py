from app.models.gift import Gift
from app.schemas.gift import GiftResponse
from app.services.ecommerce.link_builder import default_platform_links


def serialize_gift(gift: Gift) -> dict:
    payload = GiftResponse.model_validate(gift).model_dump()
    links = default_platform_links(gift.name)
    if not payload.get("purchase_url"):
        platform = payload.get("platform") or "taobao"
        payload["purchase_url"] = links.get(platform, links["taobao"])
    payload["platform_links"] = links
    return payload
