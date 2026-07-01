import json


PRODUCT_TAGS_SYSTEM_PROMPT = """
你是 Gift AI Enterprise 的电商商品标签专家。

你的任务是根据商品信息生成适合电商系统使用的商品标签。

必须严格输出 JSON。

不要输出 Markdown。
不要输出解释。
不要输出 ```json。

格式必须如下：

{
  "tags":[]
}

要求：
1. 标签必须是中文；
2. 标签数量 5-10 个；
3. 标签要简短；
4. 不要重复；
5. 不要生成虚假功效标签；
6. 适合搜索、筛选、推荐使用。
"""


def build_product_tags_prompt(
    name: str,
    category_name: str | None = None,
    brand_name: str | None = None,
    description: str | None = None,
    price: float | None = None,
) -> str:
    product = {
        "name": name,
        "category": category_name,
        "brand": brand_name,
        "description": description,
        "price": price,
    }

    return (
        "根据下面商品信息生成商品标签。\n\n"
        f"{json.dumps(product, ensure_ascii=False, indent=2)}"
    )