from pydantic import BaseModel
from typing import Literal

class SemanticMemory(BaseModel):
    category: str
    key: str
    value: str

class SemanticMemoryList(BaseModel):
    memories: list[SemanticMemory]

class MemoryOperation(BaseModel):
    action: Literal['add', 'update', 'delete']
    memory: SemanticMemory

class MemoryOperationList(BaseModel):
    operations: list[MemoryOperation]