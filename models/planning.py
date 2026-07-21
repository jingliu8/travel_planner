from models.base import StrictBaseModel

class PlanStep(StrictBaseModel):
    step: int
    description: str

class Plan(StrictBaseModel):
    goal: str
    steps: list[PlanStep]