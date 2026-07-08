from llm import LLMClient
from prompts import TRAVEL_PLANNER_SYSTEM_PROMPT, TRAVEL_USER_PROMPT
from models import TravelPlan, TravelRequest


class TravelPlanner:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def generate_itinerary(self, request: TravelRequest):

        user_input = TRAVEL_USER_PROMPT.format(
            destination=request.destination,
            days=request.days,
            interests=", ".join(request.interests)
        )
        response = self.llm.generate(
            system_prompt=TRAVEL_PLANNER_SYSTEM_PROMPT,
            user_input=user_input,
        )
        return TravelPlan.model_validate_json(response)