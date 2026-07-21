import sqlite3

class MemoryDatabase:
    def __init__(self, db_path: str='memory.db'):
        self.conn = sqlite3.connect(db_path)

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS semantic_memory (
                key TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                value TEXT NOT NULL
            )
            '''
        )
        self.conn.commit()


    def upsert(self, category: str, key: str, value: str) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE 
            INTO semantic_memory (category, key, value)
            VALUES (?, ?, ?)
            """,
            (category, key, value)
        )
        self.conn.commit()


    def delete(self, key: str) -> None:
        self.conn.execute(
            """DELETE FROM semantic_memory WHERE key = ?""",
            (key,)
        )
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute(
            """
            SELECT category, key, value FROM semantic_memory
            """
        )
        return cursor.fetchall()