import sqlite3
from typing import List, Tuple, Optional

class MemoryDatabase:
    """SQLite database for storing semantic memories."""

    DEFAULT_DB_PATH = 'memory.db'
    TABLE_NAME = 'semantic_memory'

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        """
        Initialize the memory database.
        
        Args:
            db_path: Path to SQLite database file
            
        Raises:
            ValueError: If db_path is empty
            sqlite3.Error: If database initialization fails
        """
        if not db_path:
            raise ValueError("db_path cannot be empty")
        
        self.db_path = db_path
        
        try:
            self.conn = sqlite3.connect(db_path)
            self.conn.execute('PRAGMA foreign_keys = ON')
            self._create_table()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to initialize database at {db_path}: {str(e)}")

    def _create_table(self) -> None:
        """Create the semantic_memory table if it doesn't exist."""
        try:
            self.conn.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                    key TEXT PRIMARY KEY,
                    category TEXT NOT NULL,
                    value TEXT NOT NULL
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to create table: {str(e)}")

    def upsert(self, category: str, key: str, value: str) -> None:
        """
        Insert or update a memory record.
        
        Args:
            category: Memory category
            key: Unique key for the memory
            value: Memory content/value
            
        Raises:
            ValueError: If any parameter is empty
            sqlite3.Error: If database operation fails
        """
        if not category:
            raise ValueError("category cannot be empty")
        if not key:
            raise ValueError("key cannot be empty")
        if not value:
            raise ValueError("value cannot be empty")
        
        try:
            self.conn.execute(f'''
                INSERT OR REPLACE 
                INTO {self.TABLE_NAME} (category, key, value)
                VALUES (?, ?, ?)
            ''', (category, key, value))
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            raise sqlite3.Error(f"Failed to upsert memory: {str(e)}")

    def delete(self, key: str) -> None:
        """
        Delete a memory record by key.
        
        Args:
            key: Key of the record to delete
            
        Raises:
            ValueError: If key is empty
            sqlite3.Error: If database operation fails
        """
        if not key:
            raise ValueError("key cannot be empty")
        
        try:
            self.conn.execute(f'DELETE FROM {self.TABLE_NAME} WHERE key = ?', (key,))
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            raise sqlite3.Error(f"Failed to delete memory: {str(e)}")

    def get_all(self) -> List[Tuple[str, str, str]]:
        """
        Retrieve all memory records.
        
        Returns:
            List of tuples (category, key, value)
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            cursor = self.conn.execute(f'SELECT category, key, value FROM {self.TABLE_NAME}')
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to retrieve memories: {str(e)}")

    def get_by_category(self, category: str) -> List[Tuple[str, str, str]]:
        """
        Retrieve memories by category.
        
        Args:
            category: Memory category to filter by
            
        Returns:
            List of tuples (category, key, value)
            
        Raises:
            ValueError: If category is empty
            sqlite3.Error: If database operation fails
        """
        if not category:
            raise ValueError("category cannot be empty")
        
        try:
            cursor = self.conn.execute(
                f'SELECT category, key, value FROM {self.TABLE_NAME} WHERE category = ?',
                (category,)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to retrieve memories by category: {str(e)}")

    def get_by_key(self, key: str) -> Optional[Tuple[str, str, str]]:
        """
        Retrieve a single memory by key.
        
        Args:
            key: Memory key
            
        Returns:
            Tuple (category, key, value) or None if not found
            
        Raises:
            ValueError: If key is empty
            sqlite3.Error: If database operation fails
        """
        if not key:
            raise ValueError("key cannot be empty")
        
        try:
            cursor = self.conn.execute(
                f'SELECT category, key, value FROM {self.TABLE_NAME} WHERE key = ?',
                (key,)
            )
            return cursor.fetchone()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to retrieve memory by key: {str(e)}")

    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


db = MemoryDatabase()
print(db.get_all())