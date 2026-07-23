from openai import OpenAI
from config import OPENAI_API_KEY
from models.rag import Chunk

class EmbeddingModel:
    """Embedding model using OpenAI for generating text embeddings."""
    
    DEFAULT_MODEL = 'text-embedding-3-small'

    def __init__(self, model: str = DEFAULT_MODEL):
        """
        Initialize the embedding model.
        
        Args:
            model: OpenAI embedding model name
            
        Raises:
            ValueError: If model is empty
        """
        if not model:
            raise ValueError("model cannot be empty")
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model

    def embed_text(self, text: str) -> list[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
            
        Raises:
            ValueError: If text is empty
        """
        if not text:
            raise ValueError("text cannot be empty")
        
        response = self.client.embeddings.create(model=self.model, input=text)
        return response.data[0].embedding

    def embed_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
        """
        Generate embeddings for a list of chunks.
        
        Args:
            chunks: List of chunks to embed
            
        Returns:
            Chunks with embeddings populated
            
        Raises:
            ValueError: If chunks list is empty
        """
        if not chunks:
            raise ValueError("chunks list cannot be empty")
        
        for chunk in chunks:
            chunk.embedding = self.embed_text(chunk.content)
        return chunks