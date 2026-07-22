from models.rag import Chunk
from rag.embedding import EmbeddingModel
from rag.vector_store import SupabaseVectorStore
from config import SIMILARITY_THRESHOLD, TOP_K

class Retriever:
    """Retriever for finding similar documents using vector similarity."""

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: SupabaseVectorStore,
        similarity_threshold: float = SIMILARITY_THRESHOLD,
        top_k: int = TOP_K,
    ):
        """
        Initialize the retriever.
        
        Args:
            embedding_model: Model for generating query embeddings
            vector_store: Vector store for searching documents
            similarity_threshold: Minimum similarity score for results
            top_k: Number of top results to retrieve
            
        Raises:
            ValueError: If embedding_model or vector_store is None
            ValueError: If similarity_threshold not in [0, 1] or top_k <= 0
        """
        if not embedding_model:
            raise ValueError("embedding_model cannot be None")
        if not vector_store:
            raise ValueError("vector_store cannot be None")
        if not (0 <= similarity_threshold <= 1):
            raise ValueError("similarity_threshold must be between 0 and 1")
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.similarity_threshold = similarity_threshold
        self.top_k = top_k

    def retrieve(self, query: str) -> list[Chunk]:
        """
        Retrieve documents similar to the query.
        
        Args:
            query: Query text
            
        Returns:
            List of chunks with similarity >= threshold
            
        Raises:
            ValueError: If query is empty
        """
        if not query or not query.strip():
            raise ValueError("query cannot be empty")
        
        query_embedding = self.embedding_model.embed_text(query)
        chunks = self.vector_store.search(query_embedding, self.top_k)
        return [chunk for chunk in chunks if chunk.similarity >= self.similarity_threshold]