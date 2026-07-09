# Given a question, return the most relevant chucks

from models import Chunk
from rag.embedding import EmbeddingModel
from rag.vector_store import SupabaseVectorStore

class Retriever:
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: SupabaseVectorStore
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int=3):
        query_embedding = self.embedding_model.embed_text(query)
        return self.vector_store.search(query_embedding, top_k)