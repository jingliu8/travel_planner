from models.base import StrictBaseModel
from typing import Optional, Any
from pydantic import Field

class PlanStep(StrictBaseModel):
    step: int
    description: str
    suggested_tool: Optional[str]
    tool_input: str

class Plan(StrictBaseModel):
    goal: str
    steps: list[PlanStep]