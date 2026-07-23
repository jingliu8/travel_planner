from typing import List
from models.memory import SemanticMemory, MemoryOperation
from memory.database import MemoryDatabase

class MemoryStore:
    """Store for managing memory operations and retrieval."""

    VALID_ACTIONS = {'add', 'update', 'delete'}

    def __init__(self, database: MemoryDatabase):
        """
        Initialize the memory store.
        
        Args:
            database: MemoryDatabase instance for persistence
            
        Raises:
            ValueError: If database is None
        """
        if not database:
            raise ValueError("database cannot be None")
        
        self.database = database

    def apply(self, operation: MemoryOperation) -> None:
        """
        Apply a single memory operation.
        
        Args:
            operation: MemoryOperation to apply
            
        Raises:
            ValueError: If operation is None or has invalid action
        """
        if not operation:
            raise ValueError("operation cannot be None")
        
        if operation.action not in self.VALID_ACTIONS:
            raise ValueError(f"Invalid action: {operation.action}. Must be one of {self.VALID_ACTIONS}")
        
        memory = operation.memory
        
        if operation.action in ('add', 'update'):
            self.database.upsert(
                memory.category,
                memory.key,
                memory.value,
            )
        elif operation.action == 'delete':
            self.database.delete(memory.key)

    def apply_batch(self, operations: List[MemoryOperation]) -> None:
        """
        Apply multiple memory operations in batch.
        
        Args:
            operations: List of MemoryOperation to apply
            
        Raises:
            ValueError: If operations list is empty
        """
        if not operations:
            raise ValueError("operations list cannot be empty")
        
        for operation in operations:
            self.apply(operation)

    def get_all(self) -> List[SemanticMemory]:
        """
        Get all stored memories.
        
        Returns:
            List of SemanticMemory objects
        """
        rows = self.database.get_all()
        return [
            SemanticMemory(
                category=row[0],
                key=row[1],
                value=row[2]
            ) for row in rows
        ]

    def get_by_category(self, category: str) -> List[SemanticMemory]:
        """
        Get memories by category.
        
        Args:
            category: Category to filter by
            
        Returns:
            List of SemanticMemory objects in the category
            
        Raises:
            ValueError: If category is empty
        """
        if not category:
            raise ValueError("category cannot be empty")
        
        rows = self.database.get_by_category(category)
        return [
            SemanticMemory(
                category=row[0],
                key=row[1],
                value=row[2]
            ) for row in rows
        ]

    def get_by_key(self, key: str) -> SemanticMemory:
        """
        Get a single memory by key.
        
        Args:
            key: Memory key
            
        Returns:
            SemanticMemory object or None if not found
            
        Raises:
            ValueError: If key is empty
        """
        if not key:
            raise ValueError("key cannot be empty")
        
        row = self.database.get_by_key(key)
        if not row:
            return None
        
        return SemanticMemory(
            category=row[0],
            key=row[1],
            value=row[2]
        )

