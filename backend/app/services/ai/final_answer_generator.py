from app.services.ai.deepseek_ai_service import deepseek_ai_service


class FinalAnswerGenerator:
    """
    企业级 Final Answer 合并器
    """

    SYSTEM_PROMPT = """
你是一个AI总结器。

你的任务：
- 将多个AI执行结果整合成“最终用户可读答案”
- 不要输出JSON
- 输出自然语言中文
- 简洁专业

格式要求：
- 分点总结
- 最后给结论
"""

    async def generate(self, goal: str, results: list):

        prompt = f"""
用户目标：
{goal}

执行结果：
{results}

请生成最终总结：
"""

        return await deepseek_ai_service.chat(
            prompt=prompt,
            system_prompt=self.SYSTEM_PROMPT
        )


final_answer_generator = FinalAnswerGenerator()