from supabase import create_client
from models import Chunk

class SupabaseVectorStore:

    def __init__(self, url: str, key: str):
        self.client = create_client(url, key)


    def add_documents(self, chucks: list[Chunk]) -> None:
        records = []
        for chuck in chucks:
            records.append(
                {
                    'id': chuck.id,
                    'source': chuck.source,
                    'content': chuck.content,
                    'embedding': chuck.embedding,
                }
            )
        self.client.table(
            'documents',
        ).insert(records).execute()


    def search(self, query_embedding: list[float], top_k: int=3) -> list[Chunk]:
        response = self.client.rpc(
            'match_documents',
            {
                'query_embedding': query_embedding,
                'match_count': top_k,
            }
        ).execute()

        chunks = []

        for row in response.data:
            chunks.append(
                Chunk(
                    id=row['id'],
                    source=row['source'],
                    content=row['content'],
                )
            )
        return chunks