from pydantic import BaseModel
from typing import Any, Optional, Dict


class AgentRunRequest(BaseModel):
    """
    Agent统一请求结构
    """
    user_id: str = "default"
    goal: str
    metadata: Optional[Dict[str, Any]] = None


class AgentRunResponse(BaseModel):
    """
    Agent统一响应结构
    """
    success: bool = True
    goal: str
    user_id: str
    plans: list
    steps: list
    final_answer: Any
    profile: dict = {}
    compressed_memory: dict = {}
    error: Optional[str] = None