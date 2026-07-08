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

