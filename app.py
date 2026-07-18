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
from memory.retriever import MemoryRetriever


from memory.store import MemoryStore
from memory.retriever import MemoryRetriever
from memory.extractor import MemoryExtractor



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

    # Memory
    memory_store = MemoryStore()
    memory_retriever = MemoryRetriever(memory_store)
    memory_extractor = MemoryExtractor(llm_client)

    agent = Agent(
        llm_client,
        tool_executor,
        tool_registry,
        memory_retriever,
        memory_extractor,
        memory_store
    )
    #
    # planner = TravelPlanner(retriever, agent)
    #
    # request = TravelRequest(
    #     destination='New York',
    #     days=4,
    #     interests=['hiking', 'weather', 'flight'],
    # )
    # result = planner.generate_itinerary(request)
    #
    # print("\nFinal result:")
    # print(result)
    # -------------------------
    # Test 1
    # -------------------------
    answer = agent.run(
        system_prompt="""
        You are a travel planning assistant.
        Use tools when needed.
        Return a structured travel plan.
        """,
        user_input="""
        I like hiking and nature.
        Plan a 4 day trip to Asheville.
        """,
    )

    print("\n======== ANSWER ========")
    print(answer)


    print("\n======== MEMORY ========")
    for memory in memory_store.get_all():
        print(memory)

    print("\n======== 2nd ========")
    answer = agent.run(
        system_prompt="You are a travel assistant.",
        user_input="""
        Suggest another destination for my next trip.
        """
    )
    print(answer)



if __name__ == "__main__":
    main()