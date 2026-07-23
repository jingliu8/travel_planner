import json

from llm import LLMClient
from memory.extractor import MemoryExtractor
from memory.retriever import MemoryRetriever
from memory.store import MemoryStore
from planning.planner import Planner
from models.planning import Plan
from tools.tool_executor import ToolExecutor
from tools.tool_registry import ToolRegistry

class Agent:

    def __init__(
        self,
        llm: LLMClient,
        tool_executor: ToolExecutor,
        tool_registry: ToolRegistry,
        memory_retriever: MemoryRetriever,
        memory_extractor: MemoryExtractor,
        memory_store: MemoryStore,
        planner: Planner,
        max_iterations=5
    ):
        self.llm = llm
        self.tool_executor = tool_executor
        self.tool_registry = tool_registry

        self.memory_retriever = memory_retriever
        self.memory_extractor = memory_extractor
        self.memory_store = memory_store

        self.planner = planner

        self.max_iterations = max_iterations

    def run(self, system_prompt: str, user_input: str, output_schema=None):

        plan = self.planner.create_plan(user_input)
        plan_context = '\n'.join(f'{step.step}. {step.description}' for step in plan.steps)

        print("======== PLAN ========")
        print(plan.goal)

        for step in plan.steps:
            print(step.step, step.description)

        augmented_input = self._build_augmented_input(user_input, plan, plan_context)

        response = self.llm.create_response(
            instructions=system_prompt,
            user_input=augmented_input,
            tools=self.tool_registry.get_definitions(),
            store=True
        )

        for i in range(self.max_iterations):
            print(f'========= Agent iteration {i + 1} =========')
            tool_outputs = self._execute_tools(response)

            if not tool_outputs:
                print("============ Agent finished ===========")

                answer = self._finalize_response(response, output_schema)

                memory_operations = self._extract_memory_operations(user_input)

                if len(memory_operations.operations) > 0:
                    self.memory_store.apply_batch(memory_operations.operations)

                return answer

            response = self.llm.create_response(
                previous_response_id=response.id,
                user_input=tool_outputs,
                tools=self.tool_registry.get_definitions()
            )

        raise RuntimeError('Agent exceeded maximum number of iterations')

    def _build_augmented_input(self, user_input: str, plan: Plan, plan_context: str) -> str:
        memory_context = 'No known user memories'
        memories = self.memory_retriever.retrieve(user_input)
        if memories:
            memory_context = '\n'.join([
                f'{m.key} {m.value}'
                for m in memories
            ])
        return f"""
        # User Memory
        {memory_context}
        
        # Execution Plan
        
        Goal:
        {plan.goal}
        
        Steps:
        {plan_context}
        
        # Current Request
        {user_input}
        """

    def _execute_tools(self, response):
        tool_outputs = []

        for item in response.output:

            print("TYPE", item.type)

            if item.type != "function_call":
                continue

            print("Tool Name:", item.name)
            print("Arguments:", item.arguments)

            arguments = json.loads(item.arguments)
            result = self.tool_executor.execute(item.name, arguments)

            print("Tool result:")
            print(result)

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(result),
            })

        return tool_outputs

    def _finalize_response(self, response, output_schema):
        if output_schema:
            response = self.llm.create_response(
                previous_response_id=response.id,
                user_input="Continue and provide the final answer.",
                output_schema=output_schema
            )

        return response.output_text

    def _extract_memory_operations(self, user_input: str):
        return self.memory_extractor.extract(user_input)