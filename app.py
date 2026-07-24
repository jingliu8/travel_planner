from llm import LLMClient
from agent import Agent
from planning.planner import Planner

from memory.database import MemoryDatabase


from rag.embedding import EmbeddingModel
from rag.retriever import Retriever
from rag.vector_store import SupabaseVectorStore
from config import SUPABASE_URL, SUPABASE_KEY
from tools.weather_tool import WeatherTool
from tools.search_knowledge_tool import SearchKnowledgeTool
from tools.tool_executor import ToolExecutor
from tools.tool_registry import ToolRegistry

from memory.store import MemoryStore
from memory.retriever import MemoryRetriever
from memory.extractor import MemoryExtractor

from travel.travel_planner import TravelPlanner
from travel.prompts import TRAVEL_PLANNER_SYSTEM_PROMPT
from models.tools import TravelPlan, TravelRequest


def main():
    #------------------------- Infrastructure -----------------------------
    llm = LLMClient()

    memory_db = MemoryDatabase('memory.db')
    memory_store = MemoryStore(memory_db)
    memory_retriever = MemoryRetriever(memory_store)
    memory_extractor = MemoryExtractor(llm)

    embedding_model = EmbeddingModel()
    vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_KEY)
    knowledge_retriever = Retriever(embedding_model, vector_store)

    tool_registry = ToolRegistry()
    tool_registry.register(WeatherTool())
    tool_registry.register(SearchKnowledgeTool(knowledge_retriever))
    tool_executor = ToolExecutor(tool_registry)

    #------------------------ Planner ----------------------------------
    planner = Planner(llm, tool_registry)

    #------------------------ Agent ------------------------------------
    agent = Agent(
        llm,
        tool_executor,
        tool_registry,
        memory_retriever,
        memory_extractor,
        memory_store,
        planner
    )

    #------------------------- Application -------------------------------
    travel_planner = TravelPlanner(agent)
    request = TravelRequest(
        destination='Asheville',
        days=4,
        interests=[
            'hiking',
            'nature'
        ]
    )
    itinerary = travel_planner.generate_itinerary(request)
    print(itinerary.model_dump_json(indent=2))

if __name__ == "__main__":
    main()