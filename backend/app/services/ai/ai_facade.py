from pydantic import ValidationError

from app.schemas.ai_facade import AIRequest, AIResponse
from app.services.ai.provider_router import ai_provider_router
from app.services.ai.prompt_manager import prompt_manager

from app.services.ai.ai_output_parser import ai_output_parser
from app.schemas.product_ai_result import ProductAIResult

from app.services.ai.ai_agent import ai_agent
from app.services.ai.agent_brain import agent_brain


class AIFacade:
    """
    企业级 AI Facade（统一入口）
    """

    def __init__(self):
        # 绑定 Agent & Brain
        ai_agent.facade = self
        agent_brain.facade = self

    async def execute(self, request: AIRequest) -> AIResponse:

        system_prompt = None
        user_prompt = None

        # =========================
        # Prompt 构建
        # =========================

        if request.task_type == "product_description":
            system_prompt, user_prompt = prompt_manager.build_product_description(
                name=request.context.get("name"),
                category_name=request.context.get("category_name"),
                brand_name=request.context.get("brand_name"),
                price=request.context.get("price"),
            )

        elif request.task_type == "product_tags":
            system_prompt, user_prompt = prompt_manager.build_product_tags(
                name=request.context.get("name"),
                category_name=request.context.get("category_name"),
                brand_name=request.context.get("brand_name"),
                description=request.context.get("description"),
                price=request.context.get("price"),
            )

        elif request.task_type == "image_recognition":
            system_prompt, user_prompt = prompt_manager.build_image_recognition(
                image_url=request.image_url or request.context.get("image_url", ""),
            )

        # 注入 prompt
        request.prompt = user_prompt
        request.context["system_prompt"] = system_prompt

        # =========================
        # 执行引擎选择
        # =========================

        if request.context.get("use_brain"):

            goal = request.context.get("goal") or request.prompt or "no input"

            result = await agent_brain.run(goal)

        elif request.context.get("use_agent"):

            result = await ai_agent.run_task(
                task=type("Task", (), {
                    "task_type": request.task_type,
                    "payload": request.context
                })
            )

        else:
            provider = ai_provider_router.get_provider(request)
            result = await provider.execute(request)

        # =========================
        # 输出解析层
        # =========================

        if not isinstance(result, AIResponse):
            raise TypeError("AI provider must return AIResponse")

        if isinstance(result.data, str):
            parsed = ai_output_parser.parse(result.data)

            try:
                result.data = ProductAIResult(**parsed).model_dump()
            except ValidationError:
                result.data = parsed

        return result

    def get_agent(self):
        return ai_agent

    def get_brain(self):
        return agent_brain


# 单例
ai_facade = AIFacade()
