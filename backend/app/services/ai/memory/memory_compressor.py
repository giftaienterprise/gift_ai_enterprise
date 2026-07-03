from app.services.ai.deepseek_ai_service import deepseek_ai_service
from app.services.ai.memory.redis_memory import redis_memory


class MemoryCompressor:
    """
    企业级 Memory 压缩器（长期记忆优化）
    """

    SYSTEM_PROMPT = """
你是一个AI记忆压缩器。

你的任务：
- 从用户历史对话中提取关键信息
- 删除无用内容
- 保留长期价值信息
- 总结成短记忆

输出 JSON：
{
  "summary": "...",
  "key_facts": [],
  "preferences": [],
  "important_context": []
}
"""

    async def compress(self, user_id: str):

        history = redis_memory.get_history(user_id)

        prompt = f"""
用户历史：
{history}

请压缩记忆：
"""

        result = await deepseek_ai_service.chat(
            prompt=prompt,
            system_prompt=self.SYSTEM_PROMPT
        )

        return result


memory_compressor = MemoryCompressor()