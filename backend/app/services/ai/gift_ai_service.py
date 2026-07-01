class GiftAIService:
    """
    Gift AI 服务层

    当前先做骨架，不接真实模型。
    后续负责：
    - AI 礼品描述生成
    - AI 标签生成
    - AI 图片识别
    - AI 推荐
    """

    def generate_description(
        self,
        gift_name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
    ) -> str:
        """
        生成礼品描述
        """

        parts = [gift_name]

        if category_name:
            parts.append(f"分类：{category_name}")

        if brand_name:
            parts.append(f"品牌：{brand_name}")

        return "这是一款适合作为礼品的商品，" + "，".join(parts)

    def generate_tags(
        self,
        gift_name: str,
    ) -> list[str]:
        """
        生成礼品标签
        """

        return [
            "礼品",
            "推荐",
            gift_name,
        ]


gift_ai_service = GiftAIService()