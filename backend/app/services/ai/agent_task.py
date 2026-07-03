import uuid
import time
from typing import Dict, Any


class AgentTask:
    """
    企业级 Agent Task Tracking
    """

    def __init__(self, goal: str, user_id: str):
        self.task_id = str(uuid.uuid4())
        self.goal = goal
        self.user_id = user_id

        self.status = "running"  # running / success / failed

        self.start_time = time.time()
        self.end_time = None

        self.trace = []

        self.result = None
        self.error = None

    # =========================
    # 添加执行日志
    # =========================
    def add_trace(self, step: str, data: Any = None):

        self.trace.append({
            "step": step,
            "data": data,
            "time": time.time()
        })

    # =========================
    # 成功结束
    # =========================
    def success(self, result: Any):

        self.status = "success"
        self.result = result
        self.end_time = time.time()

    # =========================
    # 失败结束
    # =========================
    def fail(self, error: str):

        self.status = "failed"
        self.error = error
        self.end_time = time.time()

    # =========================
    # 输出结构
    # =========================
    def to_dict(self):

        return {
            "task_id": self.task_id,
            "goal": self.goal,
            "user_id": self.user_id,
            "status": self.status,
            "trace": self.trace,
            "result": self.result,
            "error": self.error,
            "cost_time": (
                (self.end_time - self.start_time)
                if self.end_time else None
            )
        }