from pydantic import BaseModel

from models.base import StrictBaseModel

class TravelRequest(BaseModel):
    destination: str
    days: int
    interests: list[str]

class Activity(StrictBaseModel):
    time: str
    activity: str

class DayPlan(StrictBaseModel):
    day: int
    activities: list[Activity]
    restaurants: list[str]

class TravelPlan(StrictBaseModel):
    destination: str
    days: list[DayPlan]