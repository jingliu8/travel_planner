from typing import Optional
from pydantic import BaseModel


class Document(BaseModel):
    source: str
    content: str

class Chunk(BaseModel):
    id: str
    source: str
    content: str
    embedding: Optional[list[float]] = None
    similarity: Optional[float] = None
