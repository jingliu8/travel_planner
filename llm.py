from openai import OpenAI
from config import OPENAI_API_KEY, MODEL
from typing import Optional, Dict, Any, List

class LLMClient:
    """Client for interacting with OpenAI's API."""

    def __init__(self, client: Optional[OpenAI] = None, model: Optional[str] = None):
        """
        Initialize the LLM client.
        
        Args:
            client: OpenAI client instance (creates new one if None)
            model: Model name to use (defaults to MODEL from config)
            
        Raises:
            ValueError: If OPENAI_API_KEY is not configured
        """
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be configured in environment")
        
        self.client = client or OpenAI(api_key=OPENAI_API_KEY)
        self.model = model or MODEL

    def create_response(
        self,
        *,
        input: str,
        instructions: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        previous_response_id: Optional[str] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        store: bool = False
    ) -> Any:
        """
        Create a response from the LLM.
        
        Args:
            input: Main input/prompt for the LLM
            instructions: System instructions for the LLM
            tools: List of tool definitions available to the LLM
            previous_response_id: ID of previous response for context
            output_schema: JSON schema for structured output
            store: Whether to store the response
            
        Returns:
            Response from OpenAI API
            
        Raises:
            ValueError: If input is empty
            Exception: If API call fails
        """
        if not input:
            raise ValueError("input cannot be empty")
        
        kwargs = {
            'model': self.model,
            'input': input,
        }
        
        if instructions:
            kwargs['instructions'] = instructions
        
        if previous_response_id:
            kwargs['previous_response_id'] = previous_response_id
        
        if tools:
            kwargs['tools'] = tools
        
        if store:
            kwargs['store'] = True
        
        if output_schema:
            kwargs['text'] = {
                'format': {
                    'type': 'json_schema',
                    'name': output_schema.__name__,
                    'schema': output_schema.model_json_schema(),
                    'strict': True
                }
            }

        return self.client.responses.create(**kwargs)