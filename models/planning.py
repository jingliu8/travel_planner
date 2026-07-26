from models.base import StrictBaseModel
from typing import Optional, Any, Literal
from pydantic import Field

class PlanStep(StrictBaseModel):
    step: int
    description: str
    action_type: Literal[
        'tool',
        'user_input',
        'reasoning',
        'final_answer',
    ]
    suggested_tool: Optional[str]
    tool_arguments: dict[str, str] = Field(default_factory=dict)

class Plan(StrictBaseModel):
    goal: str
    steps: list[PlanStep]