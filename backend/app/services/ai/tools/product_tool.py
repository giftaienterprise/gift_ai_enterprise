from typing import Any, Dict

from app.services.ai.tools.base_tool import BaseTool


class ProductDescriptionTool(BaseTool):
    """
    企业级 商品描述生成 Tool
    """

    name = "product_description"
    description = "生成商品描述"

    # =========================
    # 核心执行逻辑
    # =========================
    async def execute(self, payload: Dict[str, Any]) -> Any:

        name = payload.get("name", "")
        category = payload.get("category_name", "")
        brand = payload.get("brand_name", "")
        price = payload.get("price", 0)

        # =========================
        # 模拟AI生成逻辑（后续可接LLM）
        # =========================
        title = f"{brand} {name}" if brand else name

        description = f"""
这是一款{category or '优质'}商品：
- 商品名称：{name}
- 品牌：{brand or '未知品牌'}
- 价格：{price} 元

特点：
- 高品质设计
- 优秀用户体验
- 性价比突出
"""

        return {
            "success": True,
            "data": {
                "title": title,
                "description": description.strip(),
                "price": price,
                "category": category,
                "brand": brand
            }
        }


class ProductTagsTool(BaseTool):
    """
    商品标签生成 Tool
    """

    name = "product_tags"
    description = "生成商品标签"

    async def execute(self, payload: Dict[str, Any]) -> Any:

        name = payload.get("name", "")
        category = payload.get("category_name", "")

        tags = []

        if category:
            tags.append(category)

        if "手机" in name:
            tags.append("数码")
            tags.append("电子产品")

        if "耳机" in name:
            tags.append("音频")
            tags.append("音乐设备")

        tags.append("推荐")

        return {
            "success": True,
            "data": {
                "tags": list(set(tags))
            }
        }