from typing import List, Dict, Any


class AIMemory:
    """
    企业级 AI Memory（轻量版）
    """

    def __init__(self):
        # key: user_id / session_id
        self.store: Dict[str, List[Dict[str, Any]]] = {}

    # =========================
    # 1. 存储记忆
    # =========================
    def save(self, user_id: str, role: str, content: str):

        if user_id not in self.store:
            self.store[user_id] = []

        self.store[user_id].append({
            "role": role,
            "content": content
        })

    # =========================
    # 2. 获取历史
    # =========================
    def get_history(self, user_id: str, limit: int = 10):

        return self.store.get(user_id, [])[-limit:]

    # =========================
    # 3. 构建上下文
    # =========================
    def build_context(self, user_id: str):

        history = self.get_history(user_id)

        return "\n".join(
            [f"{h['role']}: {h['content']}" for h in history]
        )


# 单例
ai_memory = AIMemory()