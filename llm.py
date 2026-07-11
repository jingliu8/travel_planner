import json
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL
from models import TravelPlan

class LLMClient():
    def __init__(self, client=None):
        self.client = client or OpenAI(api_key=OPENAI_API_KEY)
        self.model = MODEL

    def generate(self, system_prompt: str, user_input: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=user_input,
        )
        return response.output_text

    def generate_with_tools(self, system_prompt: str, user_input: str, tools: list):
        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=user_input,
            tools=tools,
            store=True
        )
        return response

    def submit_tool_results(self, previous_response_id: str, tool_outputs: list):
        response = self.client.responses.create(
            model=self.model,
            previous_response_id=previous_response_id,
            input=tool_outputs,
        )
        return response