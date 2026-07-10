from llm import LLMClient
from models import TravelRequest
from planner import TravelPlanner
from rag.embedding import EmbeddingModel
from rag.retriever import Retriever
from rag.vector_store import SupabaseVectorStore
from config import SUPABASE_URL, SUPABASE_KEY

def main():

    llm = LLMClient()

    # RAG
    embedding_model = EmbeddingModel()
    vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_KEY)
    retriever = Retriever(embedding_model, vector_store)

    # User Input + Knowledge
    planner = TravelPlanner(llm, retriever)
    request = TravelRequest(
        destination='Asheville',
        days=4,
        interests=['hiking', 'nature', 'hot springs']
    )

    # Generate Itinerary
    plan = planner.generate_itinerary(request)
    print(plan.model_dump_json(indent=2))


if __name__ == "__main__":
    main()