from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ai.ai_facade import ai_facade

router = APIRouter(prefix="/ai-brain", tags=["AI Brain"])


class GoalRequest(BaseModel):
    goal: str


@router.post("/run")
async def run_brain(req: GoalRequest):

    brain = ai_facade.get_brain()

    result = await brain.run(req.goal)

    return {
        "success": True,
        "data": result
    }