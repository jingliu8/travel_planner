import json
from typing import List, Optional

from llm import LLMClient
from memory.extractor import MemoryExtractor
from memory.retriever import MemoryRetriever
from memory.store import MemoryStore
from models.execution import ExecutionStatus, ExecutionEvent, ExecutionResult, ExecutionAction
from models.planning import Plan
from planning.planner import Planner
from executor.plan_executor import PlanExecutor
from utils.common_utils import format_execution_history


def _print_plan(plan: Plan) -> None:
    print("======== PLAN ========")
    print(plan.goal)

    for step in plan.steps:
        print(step.step, step.action_type, step.suggested_tool, step.tool_arguments, step.description,)


class Agent:

    def __init__(
        self,
        llm: LLMClient,
        plan_executor: PlanExecutor,
        memory_retriever: MemoryRetriever,
        memory_extractor: MemoryExtractor,
        memory_store: MemoryStore,
        planner: Planner,
    ):
        self.llm = llm

        self.memory_retriever = memory_retriever
        self.memory_extractor = memory_extractor
        self.memory_store = memory_store

        self.planner = planner
        self.plan_executor = plan_executor

        self.execution_state = None

    def run(self, system_prompt: str, user_input: str, output_schema=None):

        # 1. Create execution plan
        plan = self.planner.create_plan(user_input)
        _print_plan(plan)

        # 2. Execute plan
        execution = self.plan_executor.execute(plan)
        self.execution_state = execution

        if execution.status == ExecutionStatus.WAITING_FOR_USER:
            return execution

        # 3. Build final prompt
        augmented_input = self._build_augmented_input(user_input, execution.execution_history)

        # 4. Ask LLM to generate answer
        response = self.llm.create_response(
            instructions=system_prompt,
            user_input=augmented_input,
            output_schema=output_schema,
        )
        execution.final_response = response.output_text

        # 5. Extract memory
        memory_operations = self.memory_extractor.extract(user_input)
        if len(memory_operations.operations) > 0:
            self.memory_store.apply_batch(memory_operations.operations)

        return execution


    def resume(
        self,
        user_answer: str,
        system_prompt: str,
        output_schema=None,
    ) -> ExecutionResult:

        execution = self.execution_state

        if execution is None:
            raise ValueError(
                "No execution state available"
            )

        if execution.status != ExecutionStatus.WAITING_FOR_USER:
            raise ValueError(
                "Only waiting executions can be resumed"
            )

        if not user_answer or not user_answer.strip():
            raise ValueError(
                "user_answer cannot be empty"
            )

        # ==========================================
        # 1. Add user's answer into execution state
        # ==========================================
        execution.execution_history.append(
            ExecutionEvent(
                step=execution.next_step_index,
                description=execution.question or 'User input required',
                action=ExecutionAction.USER_INPUT,
                arguments=None,
                result={'answer': user_answer},
            )
        )

        # ==========================================
        # 2. Continue executing remaining plan
        # ==========================================

        new_execution = self.plan_executor.execute(
            plan=execution.plan,
            start_index=execution.next_step_index,
            previous_results=execution.execution_history,
        )

        # ==========================================
        # 3. If another user input is needed
        # ==========================================

        if new_execution.status == ExecutionStatus.WAITING_FOR_USER:
            self.execution_state = new_execution
            return new_execution

        # ==========================================
        # 4. Build final LLM context
        # ==========================================

        augmented_input = self._build_augmented_input(
            user_answer,
            new_execution.execution_history,
        )

        # ==========================================
        # 5. Generate final response
        # ==========================================

        response = self.llm.create_response(
            instructions=system_prompt,
            user_input=augmented_input,
            output_schema=output_schema,
            store=True,
        )

        # ==========================================
        # 6. Save final response and execution state
        # ==========================================

        new_execution.final_response = response.output_text

        self.execution_state = new_execution

        return new_execution


    def _build_augmented_input(
        self,
        user_input: str,
        execution_history: List[ExecutionEvent],
    ) -> str:
        #================ User Memory ==========================
        memory_context = "No known user memories"
        memories = self.memory_retriever.retrieve(user_input)

        if memories:
            memory_context = "\n".join(
                [
                    f"{m.key}: {m.value}"
                    for m in memories
                ]
            )
        #================= Execution History ====================
        execution_context = format_execution_history(execution_history)

        return f"""
        # User Request

        {user_input}

        # User Memory

        {memory_context}

        # Tool Results

        {execution_context}
        """