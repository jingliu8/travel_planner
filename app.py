from agent import Agent
from llm import LLMClient
from planner import TravelPlanner
from rag.embedding import EmbeddingModel
from rag.retriever import Retriever
from rag.vector_store import SupabaseVectorStore
from config import SUPABASE_URL, SUPABASE_KEY
from models import TravelRequest
from tools.tool_executor import ToolExecutor
from tools.tool_registry import ToolRegistry

# TODO: FOR NOW NEED TO KEEP THESE TWO IMPORT TO ADD THEM INTO REGISTRY
from tools.weather import get_weather
from tools.flight import search_flight

def main():

    llm_client = LLMClient()

    # RAG
    embedding_model = EmbeddingModel()
    vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_KEY)
    retriever = Retriever(embedding_model, vector_store)

    # Tool Registry - already populated via @tool decorators
    tool_registry = ToolRegistry()
    tool_executor = ToolExecutor(registry=tool_registry)
    agent = Agent(llm_client, tool_executor, tool_registry)

    planner = TravelPlanner(retriever, agent)

    request = TravelRequest(
        destination='New York',
        days=4,
        interests=['hiking', 'weather', 'flight'],
    )
    result = planner.generate_itinerary(request)

    print("\nFinal result:")
    print(result)


if __name__ == "__main__":
    main()