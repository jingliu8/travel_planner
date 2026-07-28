from openai import OpenAI
from config import OPENAI_API_KEY, MODEL
from typing import Optional, Dict, Any, List, Union

from models.execution import ExecutionEvent, ReasoningResult
from utils.common_utils import format_execution_history


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
        user_input: str,
        instructions: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        previous_response_id: Optional[str] = None,
        output_schema: Any = None,
        store: bool = False
    ) -> Any:
        """
        Create a response from the LLM.
        
        Args:
            user_input: Main input/prompt for the LLM
            instructions: System instructions for the LLM
            tools: List of tool definitions available to the LLM
            previous_response_id: ID of previous response for context
            output_schema: JSON schema for structured output
            store: Whether to store the response
            
        Returns:
            Response from OpenAI API
        """
        if not user_input:
            raise ValueError("input cannot be empty")
        
        kwargs = {
            'model': self.model,
            'input': user_input,
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
                    'strict': True,
                    'schema': output_schema.model_json_schema()
                }
            }

        return self.client.responses.create(**kwargs)


    def create_reasoning(
        self,
        instruction: str,
        execution_history: List[ExecutionEvent],
    ) -> ReasoningResult:
        """
        Execute a reasoning step based on current execution state.

        The reasoning step produces a decision summary,
        not private chain-of-thought.
        """

        history_text = format_execution_history(execution_history)

        prompt = f"""
        You are the decision-making module inside an AI agent.

        Your responsibility is to make planning decisions.

        You are NOT responsible for generating the final answer,
        writing the itinerary, or producing user-facing content.

        Instead, your job is to:
        1. Analyze the current execution history.
        2. Make the next planning decision.
        3. Explain why.
        4. Recommend what the agent should do next.

        Current execution history:

        {history_text}

        Current reasoning task:

        {instruction}

        Return ONLY valid JSON:

        {{
            "decision": "the planning decision",
            "reason": "why this decision was made",
            "next_action": "what the agent should do next"
        }}
        """


        response = self.create_response(
            instructions=(
                "You are a decision-making module inside an AI agent. "
                "Return only valid JSON."
            ),
            user_input=prompt,
        )

        return ReasoningResult.model_validate_json(response.output_text)
