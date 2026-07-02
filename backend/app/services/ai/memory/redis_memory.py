import json
from typing import Dict, Any, List


class RedisMemory:
    """
    简化版 Redis Memory（当前项目兼容 Brain 使用）
    """

    def __init__(self):
        # 这里先用内存模拟 Redis（避免你当前环境依赖问题）
        self.store: Dict[str, List[Dict[str, Any]]] = {}

    async def save_interaction(
        self,
        user_id: str,
        query: str,
        answer: str
    ):
        """
        保存对话记录
        """

        if user_id not in self.store:
            self.store[user_id] = []

        self.store[user_id].append({
            "query": query,
            "answer": answer
        })

        # 限制长度（防止爆内存）
        if len(self.store[user_id]) > 20:
            self.store[user_id] = self.store[user_id][-20:]

    async def get_recent_context(self, user_id: str):
        """
        Brain 需要的上下文接口（关键修复点）
        """

        history = self.store.get(user_id, [])

        # 简单压缩记忆
        summary = "\n".join([
            f"Q: {item['query']}\nA: {item['answer']}"
            for item in history[-5:]
        ])

        return {
            "user_id": user_id,
            "history": history,
            "summary": summary
        }


# 单例
redis_memory = RedisMemory()