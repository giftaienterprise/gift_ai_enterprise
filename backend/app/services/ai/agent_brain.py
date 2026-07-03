import asyncio
import json
from typing import Any, Dict, List

from app.services.ai.tools.tool_registry import tool_registry
from app.services.ai.memory.redis_memory import redis_memory


class AgentBrain:
    """
    Step 13 Brain
    """

    def __init__(self):
        self.tool_registry = tool_registry
        self.memory = redis_memory
        self.facade = None

    async def run(self, user_input: str):

        memory_context = await self.memory.get_recent_context("default")

        from app.services.ai.llm_service import llm_service

        plan_prompt = f"""
用户问题：
{user_input}

请拆解任务为 JSON：
{{
  "tasks": [
    {{
      "tool": "tool_name",
      "params": {{}}
    }}
  ]
}}

只输出JSON
"""

        plan_result = await llm_service.chat_completion(
            messages=[
                {"role": "system", "content": "task planner"},
                {"role": "user", "content": plan_prompt}
            ],
            temperature=0.2
        )

        try:
            plan = json.loads(plan_result)
        except Exception:
            plan = {"tasks": []}

        tasks = plan.get("tasks", [])

        results = await self._execute_tasks_parallel(tasks)

        return await self._merge_final_answer(
            query=user_input,
            memory=memory_context,
            tool_results=results
        )

    async def _execute_tasks_parallel(self, tasks: List[Dict[str, Any]]):

        async def run_task(task):
            return {
                "tool": task.get("tool"),
                "result": {"mock": True}
            }

        return await asyncio.gather(*[run_task(t) for t in tasks])

    async def _merge_final_answer(self, query, memory, tool_results):

        from app.services.ai.llm_service import llm_service

        prompt = f"""
问题：
{query}

记忆：
{memory}

结果：
{json.dumps(tool_results, ensure_ascii=False, indent=2)}

请生成最终答案
"""

        return await llm_service.chat_completion(
            messages=[
                {"role": "system", "content": "assistant"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )


# ⚠️ 这一行必须存在（你现在就是缺这个）
agent_brain = AgentBrain()