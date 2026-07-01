from app.services.ai.prompts.product_description import (
    PRODUCT_DESCRIPTION_SYSTEM_PROMPT,
    build_product_description_prompt,
)
from app.services.ai.prompts.product_tags import (
    PRODUCT_TAGS_SYSTEM_PROMPT,
    build_product_tags_prompt,
)
from app.services.ai.prompts.image_recognition import (
    IMAGE_RECOGNITION_SYSTEM_PROMPT,
    build_image_recognition_prompt,
)
from app.services.ai.prompts.product_analysis import (
    PRODUCT_ANALYSIS_SYSTEM_PROMPT,
    build_product_analysis_prompt,
)

class PromptManager:
    """
    AI Prompt 统一管理器
    """

    def build_product_description(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        price: float | None = None,
    ) -> tuple[str, str]:
        system_prompt = PRODUCT_DESCRIPTION_SYSTEM_PROMPT

        user_prompt = build_product_description_prompt(
            name=name,
            category_name=category_name,
            brand_name=brand_name,
            price=price,
        )

        return system_prompt, user_prompt

    def build_product_tags(
        self,
        name: str,
        category_name: str | None = None,
        brand_name: str | None = None,
        description: str | None = None,
        price: float | None = None,
    ) -> tuple[str, str]:
        """
        构建 AI 商品标签 Prompt
        """

        system_prompt = PRODUCT_TAGS_SYSTEM_PROMPT

        user_prompt = build_product_tags_prompt(
            name=name,
            category_name=category_name,
            brand_name=brand_name,
            description=description,
            price=price,
        )

        return system_prompt, user_prompt

    def build_image_recognition(
        self,
        image_url: str,
    ) -> tuple[str, str]:
        """
        构建 AI 图片识别 Prompt
        """

        system_prompt = IMAGE_RECOGNITION_SYSTEM_PROMPT

        user_prompt = build_image_recognition_prompt(
            image_url=image_url,
        )

        return system_prompt, user_prompt

    def build_product_analysis(
            self,
            name: str,
            category_name: str | None = None,
            brand_name: str | None = None,
            description: str | None = None,
            price: float | None = None,
            image_url: str | None = None,
    ) -> tuple[str, str]:
        system_prompt = PRODUCT_ANALYSIS_SYSTEM_PROMPT

        user_prompt = build_product_analysis_prompt(
            name=name,
            category_name=category_name,
            brand_name=brand_name,
            description=description,
            price=price,
            image_url=image_url,
        )

        return system_prompt, user_prompt

prompt_manager = PromptManager()