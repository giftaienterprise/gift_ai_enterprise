class AIModelRouter:
    """
    企业级 AI 多模型路由器
    """

    def __init__(self):
        self.models = ["deepseek"]  # 后续扩展 gpt / qwen

    def select_model(self, request) -> str:
        """
        根据任务选择模型
        """

        # 默认策略
        if request.task_type == "image_recognition":
            return "deepseek"

        if request.task_type == "product_description":
            return "deepseek"

        if request.task_type == "product_tags":
            return "deepseek"

        return "deepseek"


ai_model_router = AIModelRouter()