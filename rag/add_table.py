from rag.loader import DocumentLoader
from rag.splitter import TextSplitter
from rag.embedding import EmbeddingModel
from rag.vector_store import SupabaseVectorStore
from config import SUPABASE_URL, SUPABASE_KEY


def main():

    loader = DocumentLoader("../knowledge")
    splitter = TextSplitter()
    embedding_model = EmbeddingModel()
    vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_KEY)

    print("Loading documents...")
    documents = loader.load_documents()

    print(f"Loaded {len(documents)} documents")

    print("Splitting documents...")
    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    print("Generating embeddings...")
    chunks = embedding_model.embed_chunks(chunks)

    print("Uploading embeddings...")
    vector_store.add_documents(chunks)

    print("Done.")


if __name__ == "__main__":
    main()