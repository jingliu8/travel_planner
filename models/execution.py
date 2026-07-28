from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field
from models.planning import Plan

class ExecutionStatus(str, Enum):
    COMPLETED = "completed"
    WAITING_FOR_USER = "waiting_for_user"

class ExecutionEvent(BaseModel):
    step: int
    description: str
    action: str
    arguments: Optional[Any] = None
    result: Optional[Any] = None

class ExecutionResult(BaseModel):
    status: ExecutionStatus
    plan: Plan
    next_step_index: int
    execution_history: list[ExecutionEvent] = Field(default_factory=list)
    question: Optional[str] = None
    final_response: Optional[str] = None