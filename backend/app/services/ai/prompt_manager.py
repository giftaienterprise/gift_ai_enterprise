class PromptManager:
    """
    企业级 Prompt 管理器（Sprint 11 完整版）
    """

    PROMPT_VERSION = "v1"

    # =================================================
    # 商品描述
    # =================================================
    def build_product_description(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        price: float | None = None,
    ) -> tuple[str, str]:

        system_prompt = f"""
[Prompt Version: {self.PROMPT_VERSION}]

你是企业级商品AI生成系统。

必须严格输出 JSON，不允许任何解释、Markdown或多余文本。

输出结构必须是：

{{
  "title": "",
  "subtitle": "",
  "description": "",
  "selling_points": []
}}
"""

        user_prompt = f"""
商品信息：

名称：{name}
类别：{category_name}
品牌：{brand_name}
价格：{price}

请生成标准商品描述JSON。
"""

        return system_prompt, user_prompt

    # =================================================
    # 商品标签
    # =================================================
    def build_product_tags(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        description: str | None = None,
        price: float | None = None,
    ) -> tuple[str, str]:

        system_prompt = f"""
[Prompt Version: {self.PROMPT_VERSION}]

你是企业级商品标签生成AI。

必须只输出 JSON 数组，不允许任何解释。

格式：
["标签1", "标签2", "标签3"]
"""

        user_prompt = f"""
商品信息：

名称：{name}
类别：{category_name}
品牌：{brand_name}
描述：{description}
价格：{price}

生成10个商品标签。
"""

        return system_prompt, user_prompt

    # =================================================
    # 图片识别
    # =================================================
    def build_image_recognition(
        self,
        image_url: str,
    ) -> tuple[str, str]:

        system_prompt = f"""
[Prompt Version: {self.PROMPT_VERSION}]

你是企业级图像识别AI。

必须严格输出 JSON，不允许任何解释。

输出格式：
{{
  "objects": [],
  "scene": "",
  "tags": []
}}
"""

        user_prompt = f"""
请分析图片：

{image_url}
"""

        return system_prompt, user_prompt


# 单例
prompt_manager = PromptManager()