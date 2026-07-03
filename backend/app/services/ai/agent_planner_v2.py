import json

from app.services.ai.deepseek_ai_service import deepseek_ai_service


class AgentPlannerV2:
    """
    企业级 LLM Planner v2（Memory + Tool + 智能决策版）
    """

    # =========================
    # System Prompt（核心升级）
    # =========================
    SYSTEM_PROMPT = """
你是一个企业级AI任务规划器（Agent Planner）。

你的任务：
你必须根据以下信息进行任务拆解：

1. 用户目标
2. 用户历史记忆
3. 用户画像

你必须：
- 自动判断是否需要工具
- 自动选择工具
- 自动拆解任务
- 输出结构化JSON

可用工具：
- product_description（生成商品描述）
- product_tags（生成商品标签）
- image_recognition（图片识别）

规则：
- tool 字段可以为 null（如果不需要工具）
- 必须输出 JSON 数组
- 不允许输出解释文字
- 不允许 Markdown

输出格式：

[
  {
    "task_type": "xxx",
    "tool": "xxx 或 null",
    "payload": {}
  }
]
"""

    # =========================
    # 主方法
    # =========================
    async def plan(self, goal: str):

        # =========================
        # Prompt构造（增强上下文）
        # =========================
        user_prompt = f"""
用户目标：
{goal}

请生成执行计划（严格JSON格式）：
"""

        # =========================
        # 调用LLM（DeepSeek）
        # =========================
        result = await deepseek_ai_service.chat(
            prompt=user_prompt,
            system_prompt=self.SYSTEM_PROMPT
        )

        # =========================
        # JSON解析（容错机制）
        # =========================
        try:
            plans = json.loads(result)

            # 基础校验
            if not isinstance(plans, list):
                raise ValueError("Planner output is not list")

            return plans

        except Exception:

            # =========================
            # fallback（防止LLM失败）
            # =========================
            return [
                {
                    "task_type": "product_description",
                    "tool": "product_description",
                    "payload": {"name": goal}
                }
            ]


# 单例
agent_planner_v2 = AgentPlannerV2()