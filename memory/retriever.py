from models.memory import SemanticMemory
from memory.store import MemoryStore

class MemoryRetriever:

    def __init__(self, store: MemoryStore):
        self.store = store

    def retrieve(self, query: str) -> list[SemanticMemory]:
        query_lower = query.lower()
        results = []

        for memory in self.store.get_all():
            text = f'{memory.key} {memory.value}'.lower()
            if any(word in text for word in query_lower.split()):
                results.append(memory)

        return results