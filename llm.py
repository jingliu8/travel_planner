import json
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL
from models import TravelPlan

class LLMClient:
    def __init__(self, client=None):
        self.client = client or OpenAI(api_key=OPENAI_API_KEY)
        self.model = MODEL

    def create_response(
        self,
        *,
        input,
        instructions=None,
        tools=None,
        previous_response_id=None,
        output_schema=None,
        store=False
    ):
        kwargs = {
            'model': self.model,
            'input': input,
        }
        if instructions: kwargs['instructions'] = instructions
        if previous_response_id: kwargs['previous_response_id'] = previous_response_id
        if tools: kwargs['tools'] = tools
        if store: kwargs['store'] = True
        if output_schema: kwargs['text'] = {
            'format': {
                'type': 'json_schema',
                'name': 'travel_plan',
                'schema': output_schema,
                'strict': True
            }
        }
        return self.client.responses.create(**kwargs)