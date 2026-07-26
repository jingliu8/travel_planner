import json
from typing import Any, Optional

from models.execution_result import ExecutionResult, ExecutionStatus
from models.planning import Plan, PlanStep
from tools.tool_executor import ToolExecutor


class PlanExecutor:

    def __init__(self, tool_executor: ToolExecutor):
        self.tool_executor = tool_executor

    def execute(
        self,
        plan: Plan,
        start_index: int = 0,
        previous_results: Optional[list[Any]] = None,
    ) -> ExecutionResult:
        """
        Execute all tool steps in the plan.

        Non-tool steps are skipped.
        """

        results = previous_results or []

        for step in plan.steps[start_index:]:

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
                return ExecutionResult(
                    status=ExecutionStatus.WAITING_FOR_USER,
                    plan=plan,
                    next_step_index=plan.steps.index(step) + 1,
                    tool_results=results,
                    question=step.description,
                )
            #=============== Final Answer =====================
            elif step.action_type == 'final_answer':
                print('Final answer step reached')
                break

        return ExecutionResult(
            status=ExecutionStatus.COMPLETED,
            plan=plan,
            next_step_index=len(plan.steps),
            tool_results=results,
        )