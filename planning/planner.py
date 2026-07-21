from llm import LLMClient
from models.planning import Plan


class Planner:

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def create_plan(self, user_input: str) -> Plan:
        response = self.llm.create_response(
            instructions="""
            You are a planning agent.
            Break the user's request into clear steps.
            Do not execute the steps.
            Only create a plan.
            """,
            input=user_input,
            output_schema=Plan
        )
        return Plan.model_validate_json(response.output_text)