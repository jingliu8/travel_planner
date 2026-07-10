from rag.loader import DocumentLoader
from rag.splitter import TextSplitter
from rag.embedding import EmbeddingModel
from rag.vector_store import SupabaseVectorStore
from rag.retriever import Retriever
from config import SUPABASE_URL, SUPABASE_KEY

# # Load
# loader = DocumentLoader("knowledge")
# documents = loader.load_documents()
#
# # Split
# splitter = TextSplitter(
#     chunk_size=300,
#     chunk_overlap=50
# )
# chunks = splitter.split_documents(documents)
#
# # Embed
embedding_model = EmbeddingModel()
# embedded_chunks = embedding_model.embed_chunks(chunks)
#
# Store
store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_KEY)
# store.add_documents(embedded_chunks)

# Retriever
retriever = Retriever(
    embedding_model,
    store
)

chunks = retriever.retrieve(
    "I like hiking near Asheville."
)

for chunk in chunks:
    print("=" * 50)
    print(chunk.source)
    print(chunk.content)
    print(chunk.similarity)