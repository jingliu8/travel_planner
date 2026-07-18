from memory.models import SemanticMemory, MemoryOperation

class MemoryStore:

    def __init__(self):
        self.memories: dict[str, SemanticMemory] = {}


    def apply(self, operation: MemoryOperation):
        key = operation.action
        if operation.action == 'add':
            if key not in self.memories:
                self.memories[key] = operation.memory

        if operation.action == 'update':
            self.memories[key] = operation.memory

        if operation.action == 'delete':
            self.memories.pop(key, None)

    def apply_batch(self, operations: list[MemoryOperation]):
        for operation in operations:
            self.apply(operation)

    def get_all(self):
        return list(self.memories.values())

