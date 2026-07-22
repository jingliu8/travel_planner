from prompts import TRAVEL_PLANNER_SYSTEM_PROMPT, TRAVEL_USER_PROMPT
from models.tools import TravelPlan, TravelRequest
from rag.retriever import Retriever
from agent import Agent
from tools.tool_executor import ToolExecutor
from tools.tool_registry import ToolRegistry

class TravelPlanner:

    def __init__(
        self,
        retriever: Retriever,
        agent: Agent,
    ):
        self.retriever = retriever
        self.agent = agent

    def generate_itinerary(self, request: TravelRequest):
        query = f"""
                Destination: {request.destination}
                Days: {request.days}
                Interests: {', '.join(request.interests)}
                """
        chunks = self.retriever.retrieve(query)

        if not chunks:
            context = 'No relevant knowledge was found'
        else:
            context = '\n\n'.join(chunk.content for chunk in chunks)

        for chunk in chunks:
            print(chunk.source)
            print(chunk.content)
            print(chunk.similarity)
            print("-" * 40)

        user_input = TRAVEL_USER_PROMPT.format(
            context=context,
            destination=request.destination,
            days=request.days,
            interests=", ".join(request.interests)
        )

        response = self.agent.run(
            system_prompt=TRAVEL_PLANNER_SYSTEM_PROMPT,
            user_input=user_input,
            output_schema=TravelPlan.model_json_schema(),
        )
        # print("======== RAW RESPONSE ========")
        # print(response)
        # print("==============================")
        return TravelPlan.model_validate_json(response)