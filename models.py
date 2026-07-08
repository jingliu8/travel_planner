from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class TravelRequest(BaseModel):
    destination: str
    days: int
    interests: list[str]

@dataclass
class DayPlan(BaseModel):
    day: int
    activities: list[str]
    restaurants: list[str]

@dataclass
class TravelPlan(BaseModel):
    destination: str
    days: list[DayPlan]