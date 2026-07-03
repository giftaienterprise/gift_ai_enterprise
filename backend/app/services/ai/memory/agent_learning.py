import json
from typing import Dict, Any

from app.services.ai.memory.redis_memory import redis_memory


class AgentLearning:
    """
    企业级 Agent 自学习系统

    功能：
    - 记录成功/失败路径
    - 优化 Tool 使用策略
    - 未来决策增强
    """

    # =========================
    # 记录执行结果
    # =========================
    def record(self, user_id: str, goal: str, plan: list, result: dict):

        key = f"agent_learning:{user_id}"

        data = {
            "goal": goal,
            "plan": plan,
            "result": result,
            "success": self._judge_success(result)
        }

        redis_memory.client.rpush(
            key,
            json.dumps(data, ensure_ascii=False)
        )

        redis_memory.client.ltrim(key, -100, -1)

    # =========================
    # 判断成功/失败（简单规则版）
    # =========================
    def _judge_success(self, result: dict) -> bool:

        if not result:
            return False

        if isinstance(result, dict):

            if "error" in str(result).lower():
                return False

            if "success" in result:
                return bool(result["success"])

        return True

    # =========================
    # 获取学习数据
    # =========================
    def get_learning_history(self, user_id: str):

        key = f"agent_learning:{user_id}"

        data = redis_memory.client.lrange(key, 0, -1)

        return [json.loads(i) for i in data]


agent_learning = AgentLearning()