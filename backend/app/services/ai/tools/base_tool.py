from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """
    企业级 Tool 基类（所有工具必须继承）

    作用：
    - 统一 Tool 接口
    - 规范 execute 方法
    - 支持自动注册（ToolRegistry识别）
    """

    # =========================
    # Tool 名称（必须定义）
    # =========================
    name: str = ""

    # =========================
    # Tool 描述（可选）
    # =========================
    description: str = ""

    # =========================
    # 执行入口（必须实现）
    # =========================
    @abstractmethod
    async def execute(self, payload: Dict[str, Any]) -> Any:
        """
        执行 Tool 逻辑

        Args:
            payload: 输入参数

        Returns:
            Any: Tool执行结果
        """
        pass

    # =========================
    # 安全校验（可选扩展）
    # =========================
    def validate(self, payload: Dict[str, Any]) -> bool:
        """
        默认校验（子类可覆盖）
        """
        return True

    # =========================
    # 统一执行入口（框架层调用）
    # =========================
    async def run(self, payload: Dict[str, Any]) -> Any:

        if not self.validate(payload):
            return {
                "success": False,
                "error": "Invalid payload"
            }

        return await self.execute(payload)