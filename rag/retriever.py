from models import Chunk
from rag.embedding import EmbeddingModel
from rag.vector_store import SupabaseVectorStore
from config import SIMILARITY_THRESHOLD, TOP_K

class Retriever:
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: SupabaseVectorStore,
        similarity_threshold: float = SIMILARITY_THRESHOLD,
        top_k: int = TOP_K,
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.similarity_threshold = similarity_threshold
        self.top_k = top_k

    def retrieve(self, query: str) -> list[Chunk]:
        query_embedding = self.embedding_model.embed_text(query)
        chunks = self.vector_store.search(query_embedding, self.top_k)
        return [chunk for chunk in chunks if chunk.similarity >= self.similarity_threshold]