from agent import Agent
from llm import LLMClient
from planning.planner import Planner
from rag.embedding import EmbeddingModel
from rag.retriever import Retriever
from rag.vector_store import SupabaseVectorStore
from config import SUPABASE_URL, SUPABASE_KEY
from tools.tool_executor import ToolExecutor
from tools.tool_registry import ToolRegistry

from memory.store import MemoryStore
from memory.retriever import MemoryRetriever
from memory.extractor import MemoryExtractor

from prompts import TRAVEL_PLANNER_SYSTEM_PROMPT
from models.tools import TravelPlan

# TODO: FOR NOW NEED TO KEEP THESE TWO IMPORT TO ADD THEM INTO REGISTRY
from tools.weather import get_weather
from tools.flight import search_flight

def main():

    llm_client = LLMClient()

    # RAG
    # embedding_model = EmbeddingModel()
    # vector_store = SupabaseVectorStore(SUPABASE_URL, SUPABASE_KEY)
    # retriever = Retriever(embedding_model, vector_store)

    # Tool Registry - already populated via @tool decorators
    tool_registry = ToolRegistry()
    tool_executor = ToolExecutor(registry=tool_registry)

    # Memory
    memory_store = MemoryStore()
    memory_retriever = MemoryRetriever(memory_store)
    memory_extractor = MemoryExtractor(llm_client)

    # Planner
    planner = Planner(llm_client)

    agent = Agent(
        llm_client,
        tool_executor,
        tool_registry,
        memory_retriever,
        memory_extractor,
        memory_store,
        planner
    )

    answer = agent.run(
        system_prompt=TRAVEL_PLANNER_SYSTEM_PROMPT,
        user_input="""
        Plan a 4-day hiking trip to Asheville in late October.
        I want beautiful scenery, moderate hikes, and good local food.
        """,
        output_schema=TravelPlan,
    )

    print(answer)


if __name__ == "__main__":
    main()