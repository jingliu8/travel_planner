from openai.resources.containers.files import content

from llm import LLMClient
from prompts import TRAVEL_PLANNER_SYSTEM_PROMPT, TRAVEL_USER_PROMPT
from models import TravelPlan, TravelRequest
from rag.retriever import Retriever


class TravelPlanner:
    def __init__(self, llm_client: LLMClient, retriever: Retriever) -> None:
        self.llm = llm_client
        self.retriever = retriever

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
        # print("=" * 60)
        # print("Retrieved Chunks")
        # print("=" * 60)
        #
        # for chunk in chunks:
        #     print(chunk.source)
        #     print(chunk.content)
        #     print("-" * 40)

        user_input = TRAVEL_USER_PROMPT.format(
            context=context,
            destination=request.destination,
            days=request.days,
            interests=", ".join(request.interests)
        )
        response = self.llm.generate(
            system_prompt=TRAVEL_PLANNER_SYSTEM_PROMPT,
            user_input=user_input,
        )
        return TravelPlan.model_validate_json(response)