import json
from app.services.ai.deepseek_ai_service import deepseek_ai_service
from app.services.ai.memory.redis_memory import redis_memory


class MemoryIntelligence:
    """
    AI Memory 智能分析器（用户画像 + 总结）
    """

    SYSTEM_PROMPT = """
你是一个用户画像分析AI。

你需要：
1. 从对话中提取用户偏好
2. 提取用户长期兴趣
3. 提取关键事实
4. 输出JSON

格式：
{
  "preferences": [],
  "interests": [],
  "facts": [],
  "summary": ""
}
"""

    async def analyze(self, user_id: str):

        history = redis_memory.get_history(user_id)

        prompt = f"""
用户历史对话：
{history}

请生成用户画像：
"""

        result = await deepseek_ai_service.chat(
            prompt=prompt,
            system_prompt=self.SYSTEM_PROMPT
        )

        try:
            profile = json.loads(result)

            redis_memory.update_profile(user_id, profile)

            return profile

        except Exception:

            return {
                "preferences": [],
                "interests": [],
                "facts": [],
                "summary": "无法解析"
            }


memory_intelligence = MemoryIntelligence()