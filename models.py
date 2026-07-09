from pydantic import BaseModel
from typing import Optional

class TravelRequest(BaseModel):
    destination: str
    days: int
    interests: list[str]

class DayPlan(BaseModel):
    day: int
    activities: list[str]
    restaurants: list[str]

class TravelPlan(BaseModel):
    destination: str
    days: list[DayPlan]

class Document(BaseModel):
    source: str
    content: str

class Chunk(BaseModel):
    id: str
    source: str
    content: str
    embedding: Optional[list[float]] = None