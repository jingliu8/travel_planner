from agent import Agent
from models.execution import ExecutionStatus
from models.tools import TravelPlan, TravelRequest
from travel.prompts import TRAVEL_USER_PROMPT, TRAVEL_PLANNER_SYSTEM_PROMPT

class TravelPlanner:
    def __init__(self, agent: Agent):
        """
        Initialize the travel planner.

        Args:
            agent: Agent responsible for reasoning and tool execution.

        Raises:
            ValueError: If agent is None.
        """

        if not agent:
            raise ValueError("agent cannot be None")

        self.agent = agent


    def generate_itinerary(self, request: TravelRequest):
        """
        Generate a travel itinerary from a travel request.

        Args:
            request: User travel request.

        Returns:
            Generated travel itinerary.
        """
        user_input = TRAVEL_USER_PROMPT.format(
            destination=request.destination,
            days=request.days,
            interests=', '.join(request.interests)
        )

        execution = self.agent.run(
            system_prompt=TRAVEL_PLANNER_SYSTEM_PROMPT,
            user_input=user_input,
            output_schema=TravelPlan,
        )
        if execution.status == ExecutionStatus.WAITING_FOR_USER:
            return execution

        return TravelPlan.model_validate_json(execution.final_response)
