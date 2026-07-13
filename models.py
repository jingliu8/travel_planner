from typing import Optional
from pydantic import BaseModel

################## RAG #####################
class Document(BaseModel):
    source: str
    content: str

class Chunk(BaseModel):
    id: str
    source: str
    content: str
    embedding: Optional[list[float]] = None
    similarity: Optional[float] = None

################## TOOLS ########################
class TravelRequest(BaseModel):
    destination: str
    days: int
    interests: list[str]

class Activity(BaseModel):
    time: str
    activity: str

class DayPlan(BaseModel):
    day: int
    activities: list[Activity]
    restaurants: list[str]

class TravelPlan(BaseModel):
    destination: str
    days: list[DayPlan]