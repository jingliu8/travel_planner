from typing import List
from models.memory import SemanticMemory
from memory.store import MemoryStore

class MemoryRetriever:
    """Retriever for searching memories using keyword matching."""

    def __init__(self, store: MemoryStore):
        """
        Initialize the memory retriever.
        
        Args:
            store: MemoryStore instance for accessing memories
            
        Raises:
            ValueError: If store is None
        """
        if not store:
            raise ValueError("store cannot be None")
        
        self.store = store

    def retrieve(self, query: str) -> List[SemanticMemory]:
        """
        Retrieve memories matching the query keywords.
        
        Performs keyword matching by searching for query words
        in memory keys and values (case-insensitive).
        
        Args:
            query: Search query string
            
        Returns:
            List of SemanticMemory objects matching the query
        """
        if not query:
            raise ValueError("query cannot be empty")
        
        query_lower = query.lower()
        query_words = query_lower.split()
        results = []

        for memory in self.store.get_all():
            memory_text = f'{memory.key} {memory.value}'.lower()
            
            if any(word in memory_text for word in query_words):
                results.append(memory)

        return results