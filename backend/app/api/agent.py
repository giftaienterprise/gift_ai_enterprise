from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ai.agent_brain import agent_brain


router = APIRouter(prefix="/agent", tags=["Agent"])


class AgentRunRequest(BaseModel):
    goal: str = ""
    use_brain: bool = True


class AgentRunResponse(BaseModel):
    success: bool
    goal: str
    user_id: str = "default"
    plans: list = []
    steps: list = []
    final_answer: str = None
    profile: dict = {}
    compressed_memory: dict = {}
    error: str = None


@router.post("/run", response_model=AgentRunResponse)
async def run_agent(request: AgentRunRequest):

    try:
        if request.use_brain:
            result = await agent_brain.run(
                request.goal or ""
            )

            return AgentRunResponse(
                success=True,
                goal=request.goal,
                final_answer=result if isinstance(result, str) else str(result)
            )

        return AgentRunResponse(
            success=False,
            goal=request.goal,
            error="Brain not enabled"
        )

    except Exception as e:

        return AgentRunResponse(
            success=False,
            goal=request.goal,
            error=str(e)
        )