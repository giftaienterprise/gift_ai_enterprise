from typing import Any

from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    """
    企业级 AI 统一请求对象
    """

    task_type: str = Field(..., description="AI 任务类型")
    prompt: str | None = Field(default=None, description="最终 Prompt")
    context: dict[str, Any] = Field(default_factory=dict, description="业务上下文")
    image_url: str | None = Field(default=None, description="图片地址")
    provider: str | None = Field(default=None, description="指定 AI Provider")
    use_cache: bool = Field(default=True, description="是否启用缓存")


class AIResponse(BaseModel):
    """
    企业级 AI 统一响应对象
    """

    success: bool = Field(..., description="是否成功")
    task_type: str = Field(..., description="AI 任务类型")
    provider: str = Field(..., description="实际使用的 Provider")
    data: Any = Field(default=None, description="AI 返回数据")
    error: str | None = Field(default=None, description="错误信息")
    cache_hit: bool = Field(default=False, description="是否命中缓存")
    meta: dict[str, Any] = Field(default_factory=dict, description="扩展元信息")