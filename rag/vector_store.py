from supabase import create_client
from supabase.client import Client
from models.rag import Chunk

class SupabaseVectorStore:
    """Vector store using Supabase for document storage and similarity search."""

    def __init__(self, url: str, key: str):
        """
        Initialize the Supabase vector store.
        
        Args:
            url: Supabase project URL
            key: Supabase API key
            
        Raises:
            ValueError: If url or key is empty
        """
        if not url or not key:
            raise ValueError("url and key cannot be empty")
        
        self.client: Client = create_client(url, key)
        self.table_name = 'documents'

    def add_documents(self, chunks: list[Chunk]) -> None:
        """
        Add chunks to the vector store.
        
        Args:
            chunks: List of chunks to add
            
        Raises:
            ValueError: If chunks list is empty
            Exception: If insertion fails
        """
        if not chunks:
            raise ValueError("chunks list cannot be empty")
        
        records = []
        for chunk in chunks:
            records.append(
                {
                    'id': chunk.id,
                    'source': chunk.source,
                    'content': chunk.content,
                    'embedding': chunk.embedding,
                }
            )
        
        self.client.table(self.table_name).insert(records).execute()

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3
    ) -> list[Chunk]:
        """
        Search for similar documents using vector similarity.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to return
            
        Returns:
            List of similar chunks ranked by similarity
            
        Raises:
            ValueError: If query_embedding is empty or top_k <= 0
        """
        if not query_embedding:
            raise ValueError("query_embedding cannot be empty")
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        
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
                    similarity=row['similarity'],
                )
            )
        return chunks