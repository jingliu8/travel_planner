from llm import LLMClient
from prompts import TRAVEL_PLANNER_SYSTEM_PROMPT

class TravelPlanner:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def generate_itinerary(self, user_request: str):

        return self.llm.generate(
            system_prompt=TRAVEL_PLANNER_SYSTEM_PROMPT,
            user_input=user_request,
        )