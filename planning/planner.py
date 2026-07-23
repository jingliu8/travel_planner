import json

from llm import LLMClient
from models.planning import Plan
from planning.prompts import PLANNER_SYSTEM_PROMPT
from tools.tool_registry import ToolRegistry


class Planner:
    """Planner for breaking down user requests into actionable steps."""

    def __init__(self, llm: LLMClient, tool_registry: ToolRegistry):
        if not llm:
            raise ValueError("llm cannot be None")

        if not tool_registry:
            raise ValueError("tool_registry cannot be None")

        self.llm = llm
        self.tool_registry = tool_registry


    def create_plan(self, user_input: str) -> Plan:
        if not user_input:
            raise ValueError("user_input cannot be empty")

        available_tools = self.tool_registry.get_definitions()

        planning_input = f"""
            User Request: 
            
            {user_input}
            
            Available Tools:
            
            {json.dumps(available_tools, indent=2)}
        """

        response = self.llm.create_response(
            instructions=PLANNER_SYSTEM_PROMPT,
            user_input=planning_input,
            output_schema=Plan,
        )

        return Plan.model_validate_json(
            response.output_text
        )