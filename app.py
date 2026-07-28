from llm import LLMClient
from agent import Agent
from models.execution import ExecutionStatus
from models.tools import TravelPlan
from planning.planner import Planner
from executor.plan_executor import PlanExecutor

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
from models.tools import TravelRequest


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
    plan_executor = PlanExecutor(tool_executor)

    #------------------------ Planner ----------------------------------
    planner = Planner(llm, tool_registry)

    #------------------------ Agent ------------------------------------
    agent = Agent(
        llm,
        plan_executor,
        memory_retriever,
        memory_extractor,
        memory_store,
        planner
    )

    #------------------------- Application -------------------------------
    travel_planner = TravelPlanner(agent)
    request = TravelRequest(
        destination='Asheville',
        days=3,
        interests=[
            'hiking',
            'nature'
        ]
    )
    result = travel_planner.generate_itinerary(request)

    while result.status == ExecutionStatus.WAITING_FOR_USER:
        print(result.question)

        user_answer = input("> ")

        result = agent.resume(
            user_answer=user_answer,
            system_prompt=TRAVEL_PLANNER_SYSTEM_PROMPT,
            output_schema=TravelPlan
        )

    print(result.final_response)

if __name__ == "__main__":
    main()