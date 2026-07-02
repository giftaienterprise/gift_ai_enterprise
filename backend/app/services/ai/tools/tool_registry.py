import importlib
import pkgutil
from typing import Dict, Any


class ToolRegistry:
    """
    企业级 Tool Registry（插件自动发现版本）

    功能：
    - 自动扫描 tools 目录
    - 自动注册 Tool
    - 支持 BaseTool 标准
    - 容错机制（防止模块加载失败）
    """

    def __init__(self):
        self.tools: Dict[str, Any] = {}

        # =========================
        # 自动加载所有工具
        # =========================
        self._auto_discover_tools()

    # =========================
    # 注册 Tool
    # =========================
    def register(self, tool):
        """
        注册工具
        """
        if hasattr(tool, "name") and tool.name:
            self.tools[tool.name] = tool

    # =========================
    # 获取 Tool
    # =========================
    def get(self, name: str):
        return self.tools.get(name)

    # =========================
    # 自动扫描 tools 目录
    # =========================
    def _auto_discover_tools(self):

        import app.services.ai.tools as tools_pkg

        for _, module_name, _ in pkgutil.iter_modules(tools_pkg.__path__):

            try:
                module = importlib.import_module(
                    f"app.services.ai.tools.{module_name}"
                )

                # =========================
                # 扫描模块中的 Tool 类
                # =========================
                for attr_name in dir(module):

                    obj = getattr(module, attr_name)

                    # 判断是否是 Tool（BaseTool结构）
                    if (
                        hasattr(obj, "name")
                        and callable(getattr(obj, "execute", None))
                    ):

                        try:
                            instance = obj()

                            if instance.name:
                                self.register(instance)

                        except Exception:
                            # 单个Tool失败不影响整体系统
                            pass

            except Exception:
                # 模块加载失败保护
                continue

    # =========================
    # 调试用：查看所有工具
    # =========================
    def list_tools(self):
        return list(self.tools.keys())


# =========================
# 单例
# =========================
tool_registry = ToolRegistry()