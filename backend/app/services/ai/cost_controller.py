class AICostController:
    """
    企业级 AI 成本控制器
    """

    def estimate_tokens(self, prompt: str) -> int:
        """
        简单 token 估算（字符/4）
        """
        return len(prompt) // 4

    def check_limit(self, prompt: str, limit: int) -> bool:
        tokens = self.estimate_tokens(prompt)
        return tokens <= limit


ai_cost_controller = AICostController()