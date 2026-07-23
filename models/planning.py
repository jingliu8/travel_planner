from models.base import StrictBaseModel
from typing import Optional

class PlanStep(StrictBaseModel):
    step: int
    description: str
    suggested_tool: Optional[str]

class Plan(StrictBaseModel):
    goal: str
    steps: list[PlanStep]