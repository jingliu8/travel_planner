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

            if not step.suggested_tool:
                continue

            arguments = self._build_arguments(step)

            result = self.tool_executor.execute(
                step.suggested_tool,
                arguments
            )

            results.append(result)

        return results

    # TODO: REFACTOR
    def _build_arguments(self, step: PlanStep) -> dict[str, Any]:
        """
        Convert planner output into tool arguments.

        The planner only knows the tool name and a simple tool_input.
        This method translates that into the argument dictionary expected
        by each tool.
        """

        if step.suggested_tool == "get_weather":
            return {
                "city": step.tool_input
            }

        if step.suggested_tool == "search_knowledge":
            return {
                "query": step.tool_input
            }

        return {}