from agent import Agent
from llm import LLMClient
from memory.database import MemoryDatabase

from planning.planner import Planner

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

from prompts import TRAVEL_PLANNER_SYSTEM_PROMPT
from models.tools import TravelPlan

def main():
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

    planner = Planner(llm, tool_registry)

    agent = Agent(
        llm,
        tool_executor,
        tool_registry,
        memory_retriever,
        memory_extractor,
        memory_store,
        planner
    )

    answer = agent.run(
        system_prompt=TRAVEL_PLANNER_SYSTEM_PROMPT,
        user_input='What are the best hiking trails near Asheville?',
        output_schema=TravelPlan
    )

    print(answer)

if __name__ == "__main__":
    main()