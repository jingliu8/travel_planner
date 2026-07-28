import json
from typing import List

from models.execution import ExecutionEvent


def format_execution_history(
    execution_history: List[ExecutionEvent],
) -> str:
    """
    Convert execution history into a readable format for LLM prompts.
    """

    if not execution_history:
        return "No execution history available."

    return "\n\n".join(
        [
            f"""
            Step: {event.step}
            
            Description:
            {event.description}
            
            Action:
            {event.action}
            
            Arguments:
            {json.dumps(event.arguments, indent=2) if event.arguments else "None"}
            
            Result:
            {json.dumps(event.result, indent=2, default=str)}
            """
            for event in execution_history
        ]
    )