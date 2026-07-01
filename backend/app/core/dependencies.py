from app.services.business.gift_business_service import gift_business_service


def get_gift_business_service():
    """
    获取 GiftBusinessService 实例
    """
    return gift_business_service