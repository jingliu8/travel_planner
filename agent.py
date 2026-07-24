from typing import Any, List

from llm import LLMClient
from memory.extractor import MemoryExtractor
from memory.retriever import MemoryRetriever
from memory.store import MemoryStore
from planning.planner import Planner
from executor.plan_executor import PlanExecutor

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

    def run(self, system_prompt: str, user_input: str, output_schema=None):

        # 1. Create execution plan
        plan = self.planner.create_plan(user_input)

        print("======== PLAN ========")
        print(plan.goal)

        for step in plan.steps:
            print(step.step, step.description, step.suggested_tool, step.tool_input)

        # 2. Execute plan
        tool_results = self.plan_executor.execute(plan)

        print("======== TOOL RESULTS ========")
        print(tool_results)

        # 3. Build final prompt
        augmented_input = self._build_augmented_input(user_input, tool_results)

        # 4. Ask LLM to generate answer
        response = self.llm.create_response(
            instructions=system_prompt,
            user_input=augmented_input,
            output_schema=output_schema,
            store=True
        )
        answer = response.output_text

        # 5. Extract memory
        memory_operations = self.memory_extractor.extract(user_input)
        if len(memory_operations.operations) > 0:
            self.memory_store.apply_batch(memory_operations.operations)

        return answer

    def _build_augmented_input(
            self,
            user_input: str,
            tool_results: List[Any]
    ) -> str:

        memory_context = "No known user memories"
        memories = self.memory_retriever.retrieve(user_input)

        if memories:
            memory_context = "\n".join(
                [
                    f"{m.key}: {m.value}"
                    for m in memories
                ]
            )

        execution_context = "No tool results"

        if tool_results:
            execution_context = "\n\n".join(
                [
                    str(result)
                    for result in tool_results
                ]
            )

        return f"""
                # User Memory
                
                {memory_context}
            
                # Tool Results
            
                {execution_context}
            
                # User Request
            
                {user_input}
                """