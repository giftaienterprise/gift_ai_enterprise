import json

PRODUCT_DESCRIPTION_SYSTEM_PROMPT = """
你是 Gift AI Enterprise 的电商商品文案专家。

你的任务是根据商品信息生成商品详情。

必须严格输出 JSON。

不要输出 Markdown。

不要输出解释。

不要输出 ```json。

格式必须如下：

{
  "title":"",
  "subtitle":"",
  "description":"",
  "selling_points":[]
}
"""


def build_product_description_prompt(
    name: str,
    category_name: str | None = None,
    brand_name: str | None = None,
    price: float | None = None,
) -> str:
    product = {
        "name": name,
        "category": category_name,
        "brand": brand_name,
        "price": price,
    }

    return (
        "根据下面商品信息生成商品详情。\n\n"
        f"{json.dumps(product, ensure_ascii=False, indent=2)}"
    )