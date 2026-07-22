from models.memory import SemanticMemory, MemoryOperation
from memory.database import MemoryDatabase

class MemoryStore:

    def __init__(self, database: MemoryDatabase):
        self.database = database

    def apply(self, operation: MemoryOperation):
        memory = operation.memory
        if operation.action in ('add', 'update'):
            self.database.upsert(
                memory.category,
                memory.key,
                memory.value,
            )
        elif operation.action == 'delete':
            self.database.delete(memory.key)

    def apply_batch(self, operations: list[MemoryOperation]):
        for operation in operations:
            self.apply(operation)

    def get_all(self):
        rows = self.database.get_all()
        return [
            SemanticMemory(
                category=row[0],
                key=row[1],
                value=row[2]
            ) for row in rows
        ]

