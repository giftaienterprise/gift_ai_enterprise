from typing import Any

from app.services.ai.tools.tool_registry import tool_registry


class ToolExecutor:
    """
    企业级 Tool 执行器
    """

    async def execute(self, tool_name: str, payload: dict[str, Any]):

        tool = tool_registry.get(tool_name)

        if not tool:
            return {
                "success": False,
                "error": f"Tool not found: {tool_name}"
            }

        return await tool.execute(payload)


tool_executor = ToolExecutor()