from dataclasses import dataclass
from typing import Any


@dataclass
class AITask:
    """
    AI任务单元
    """
    task_type: str
    payload: dict[str, Any]


class AIAgent:
    """
    企业级 AI Agent（任务执行器）
    """

    def __init__(self, facade):
        self.facade = facade

    # =========================
    # 单任务执行
    # =========================
    async def run_task(self, task: AITask):
        from app.schemas.ai_facade import AIRequest

        request = AIRequest(
            task_type=task.task_type,
            context=task.payload,
            use_cache=True,
        )

        return await self.facade.execute(request)

    # =========================
    # 多任务顺序执行
    # =========================
    async def run_pipeline(self, tasks: list[AITask]):
        results = []

        for task in tasks:
            result = await self.run_task(task)
            results.append(result)

        return results


# 单例将在 Facade 注入
ai_agent = AIAgent(None)