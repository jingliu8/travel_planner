import json
from typing import Any

from models.planning import Plan, PlanStep
from tools.tool_executor import ToolExecutor


class PlanExecutor:

    def __init__(self, tool_executor: ToolExecutor):
        self.tool_executor = tool_executor

    def execute(self, plan: Plan) -> list[Any]:
        """
        Execute all tool steps in the plan.

        Non-tool steps are skipped.
        """

        results = []

        for step in plan.steps:

            print(f"Executing Step {step.step}: {step.description}")

            #=============== Tool =============================
            if step.action_type == 'tool':
                if step.suggested_tool is None:
                    raise ValueError("Tool step {step.step} has no suggested tool")

                # arguments = self._build_arguments(step)
                result = self.tool_executor.execute(
                    step.suggested_tool,
                    step.tool_arguments
                )
                results.append({
                    'step': step.step,
                    'description': step.description,
                    'tool': step.suggested_tool,
                    'argument': step.tool_arguments,
                    'result': result,
                })
                continue
            #=============== Reasoning ========================
            elif step.action_type == 'reasoning':
                print('Reasoning step - skipped for now')
                continue
            #=============== User Input =======================
            elif step.action_type == 'user_input':
                print('User input required')
                # TODO: pause execution and ask the user.
                continue
            #=============== Final Answer =====================
            elif step.action_type == 'final_answer':
                print('Final answer step reached')
                break

        return results


    # def _build_arguments(self, step: PlanStep) -> dict[str, Any]:
    #     """
    #     Convert planner output into tool arguments.
    #
    #     Current planner contract:
    #     tool_input is a string.
    #
    #     We support:
    #     1. plain string input
    #     2. JSON string input
    #     """
    #
    #     tool_input = step.tool_input
    #
    #     if tool_input is None:
    #         return {}
    #
    #     # If planner accidentally returns JSON string,
    #     # convert it into a dictionary.
    #     try:
    #         parsed = json.loads(tool_input)
    #
    #         if isinstance(parsed, dict):
    #             return parsed
    #
    #     except json.JSONDecodeError:
    #         pass
    #
    #     # Otherwise use current string-based contract.
    #     if step.suggested_tool == "get_weather":
    #         return {
    #             "city": tool_input
    #         }
    #
    #     if step.suggested_tool == "search_knowledge":
    #         return {
    #             "query": tool_input
    #         }
    #
    #     raise ValueError(
    #         f"Unsupported tool: {step.suggested_tool}"
    #     )