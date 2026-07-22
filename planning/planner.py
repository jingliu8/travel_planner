from typing import Optional
from llm import LLMClient
from models.planning import Plan

class Planner:
    """Planner for breaking down user requests into actionable steps."""

    PLANNING_INSTRUCTIONS = """
    You are a planning agent.
    Break the user's request into clear steps.
    Do not execute the steps.
    Only create a plan.
    """

    def __init__(self, llm: LLMClient):
        """
        Initialize the planner.
        
        Args:
            llm: LLMClient instance for generating plans
            
        Raises:
            ValueError: If llm is None
        """
        if not llm:
            raise ValueError("llm cannot be None")
        
        self.llm = llm

    def create_plan(self, user_input: str) -> Plan:
        """
        Create a plan from user input.
        
        Args:
            user_input: User's request or description
            
        Returns:
            Plan object with generated steps
            
        Raises:
            ValueError: If user_input is empty or invalid
            Exception: If LLM fails or response is invalid
        """
        if not user_input or not user_input.strip():
            raise ValueError("user_input cannot be empty")
        
        try:
            response = self.llm.create_response(
                instructions=self.PLANNING_INSTRUCTIONS,
                input=user_input,
                output_schema=Plan
            )
        except Exception as e:
            raise Exception(f"Failed to create plan from LLM: {str(e)}")

        return Plan.model_validate_json(response.output_text)
