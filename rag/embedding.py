from openai import OpenAI
from config import OPENAI_API_KEY
from models.rag import Chunk

class EmbeddingModel:

    def __init__(self, model='text-embedding-3-small'):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model

    def embed_text(self, text: str) -> list[float]:
        response = self.client.embeddings.create(model=self.model, input=text)
        return response.data[0].embedding

    def embed_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
        for chunk in chunks:
            chunk.embedding = self.embed_text(chunk.content)
        return chunks