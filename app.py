# from llm import LLMClient
# from models import TravelRequest
# from planner import TravelPlanner
# from rag.embedding import EmbeddingModel
# from rag.retriever import Retriever
# from rag.vector_store import SupabaseVectorStore
# from config import SUPABASE_URL, SUPABASE_KEY
#
# def main():
#
#     llm = LLMClient()
#
#     # RAG
#     embedding_model = EmbeddingModel()
#     vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_KEY)
#     retriever = Retriever(embedding_model, vector_store)
#
#     # User Input + Knowledge
#     planner = TravelPlanner(llm, retriever)
#     request = TravelRequest(
#         destination='Asheville',
#         days=4,
#         interests=['hiking', 'nature', 'hot springs']
#     )
#
#     # Generate Itinerary
#     plan = planner.generate_itinerary(request)
#     print(plan.model_dump_json(indent=2))
#
#
# if __name__ == "__main__":
#     main()

from llm import LLMClient
from planner import TravelPlanner
from rag.embedding import EmbeddingModel
from rag.retriever import Retriever
from rag.vector_store import SupabaseVectorStore
from config import SUPABASE_URL, SUPABASE_KEY
from models import TravelRequest
from tools.tool_executor import ToolExecutor
from tools.tool_registry import ToolRegistry
from tools.tool_definitions import weather_tool, flight_tool
from tools.weather import get_weather
from tools.flight import search_flight

def create_tool_registry():
    registry = ToolRegistry()

    registry.register('get_weather', func=get_weather, definition=weather_tool)
    registry.register('search_flight', func=search_flight, definition=flight_tool)
    return registry

def main():

    llm_client = LLMClient()

    # RAG
    embedding_model = EmbeddingModel()
    vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_KEY)
    retriever = Retriever(embedding_model, vector_store)

    # Tool Registry
    tool_registry = create_tool_registry()
    tool_executor = ToolExecutor(registry=tool_registry)

    planner = TravelPlanner(llm_client, retriever, tool_executor, tool_registry)

    request = TravelRequest(
        destination='Asheville',
        days=4,
        interests=['hiking', 'weather', 'flight'],
    )
    result = planner.generate_itinerary(request)

    print("\nFinal result:")
    print(result)


if __name__ == "__main__":
    main()