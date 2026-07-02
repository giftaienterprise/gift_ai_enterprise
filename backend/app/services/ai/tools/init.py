"""
AI Tools Package

作用：
- 统一 tools 模块入口
- 触发 ToolRegistry 自动加载
- 保证插件系统正常初始化
"""

# =========================
# 导入 registry（触发自动扫描）
# =========================
from app.services.ai.tools.tool_registry import tool_registry


# =========================
# 可选：暴露 registry
# =========================
__all__ = [
    "tool_registry"
]
