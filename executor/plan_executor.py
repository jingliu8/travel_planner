import json
from typing import Any, Optional

from models.execution import ExecutionStatus, ExecutionEvent, ExecutionResult
from models.planning import Plan
from tools.tool_executor import ToolExecutor


class PlanExecutor:

    def __init__(self, tool_executor: ToolExecutor):
        self.tool_executor = tool_executor

    def execute(
        self,
        plan: Plan,
        start_index: int = 0,
        previous_results: Optional[list[ExecutionEvent]] = None,
    ) -> ExecutionResult:
        """
        Execute all tool steps in the plan.

        Non-tool steps are skipped.
        """

        results = previous_results or []

        for i in range(start_index, len(plan.steps)):
            step = plan.steps[i]

            print(f"Executing Step {step.step}: {step.description}")

            #=============== Tool =============================
            if step.action_type == 'tool':
                if step.suggested_tool is None:
                    raise ValueError(f"Tool step {step.step} has no suggested tool")

                result = self.tool_executor.execute(
                    step.suggested_tool,
                    step.tool_arguments
                )
                results.append(
                    ExecutionEvent(
                        step=step.step,
                        description=step.description,
                        action=step.suggested_tool,
                        arguments=step.tool_arguments,
                        result=result,
                    )
                )
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
                    next_step_index=i + 1,
                    execution_history=results,
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
            execution_history=results,
        )