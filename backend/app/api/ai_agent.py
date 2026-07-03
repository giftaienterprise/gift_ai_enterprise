from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ai.ai_facade import ai_facade
from app.services.ai.ai_agent import AITask

router = APIRouter(prefix="/ai-agent", tags=["AI Agent"])


class TaskRequest(BaseModel):
    task_type: str
    payload: dict


class PipelineRequest(BaseModel):
    tasks: list[TaskRequest]


@router.post("/run-task")
async def run_task(req: TaskRequest):
    agent = ai_facade.get_agent()

    result = await agent.run_task(
        AITask(task_type=req.task_type, payload=req.payload)
    )

    return {
        "success": True,
        "data": result.data
    }


@router.post("/run-pipeline")
async def run_pipeline(req: PipelineRequest):
    agent = ai_facade.get_agent()

    tasks = [
        AITask(task_type=t.task_type, payload=t.payload)
        for t in req.tasks
    ]

    results = await agent.run_pipeline(tasks)

    return {
        "success": True,
        "data": [r.data for r in results]
    }