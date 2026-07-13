from typing import Optional
from pydantic import BaseModel, ConfigDict


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
    model_config = ConfigDict(extra='forbid')
    time: str
    activity: str

class DayPlan(BaseModel):
    model_config = ConfigDict(extra='forbid')
    day: int
    activities: list[Activity]
    restaurants: list[str]

class TravelPlan(BaseModel):
    model_config = ConfigDict(extra='forbid')
    destination: str
    days: list[DayPlan]