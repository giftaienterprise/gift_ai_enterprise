from app.schemas.ai_facade import AIRequest


class AgentPlanner:
    """
    LLM级任务规划器（替代 if/else）
    """

    async def plan(self, goal: str):

        # 👉 这里先用“轻规则 + 可升级LLM”
        # 后面可以换成 GPT / DeepSeek planner

        tasks = []

        if "商品" in goal:

            tasks.append({
                "task_type": "product_description",
                "payload": {"name": goal},
                "tool": "product_description"
            })

            tasks.append({
                "task_type": "product_tags",
                "payload": {"name": goal},
                "tool": None
            })

        if "图片" in goal:

            tasks.append({
                "task_type": "image_recognition",
                "payload": {"image_url": goal},
                "tool": None
            })

        return tasks


agent_planner = AgentPlanner()