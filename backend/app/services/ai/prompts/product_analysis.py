import json


PRODUCT_ANALYSIS_SYSTEM_PROMPT = """
你是 Gift AI Enterprise 的企业级商品分析专家。

你的任务是根据商品基础信息，生成完整商品分析结果。

必须严格输出 JSON。
不要输出 Markdown。
不要输出解释。
不要输出 ```json。

格式必须如下：

{
  "title":"",
  "subtitle":"",
  "description":"",
  "selling_points":[],
  "tags":[],
  "category":"",
  "brand":"",
  "style":"",
  "keywords":[]
}

要求：
1. 输出中文；
2. 不确定的字段填写“未知”；
3. description 控制在 80-150 字；
4. selling_points 数量 4-6 个；
5. tags 数量 5-10 个；
6. keywords 数量 5-10 个；
7. 不要虚假宣传；
8. 不要生成医疗、功效、绝对化承诺。
"""


def build_product_analysis_prompt(
    name: str,
    category_name: str | None = None,
    brand_name: str | None = None,
    description: str | None = None,
    price: float | None = None,
    image_url: str | None = None,
) -> str:
    product = {
        "name": name,
        "category": category_name,
        "brand": brand_name,
        "description": description,
        "price": price,
        "image_url": image_url,
    }

    return (
        "请根据下面商品信息生成完整商品分析结果。\n\n"
        f"{json.dumps(product, ensure_ascii=False, indent=2)}"
    )