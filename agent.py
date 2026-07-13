import json
from llm import LLMClient
from tools.tool_executor import ToolExecutor
from tools.tool_registry import ToolRegistry
from prompts import TRAVEL_PLANNER_SYSTEM_PROMPT

class Agent:

    def __init__(
        self,
        llm: LLMClient,
        tool_executor: ToolExecutor,
        tool_registry: ToolRegistry,
        max_iterations=5
    ):
        self.llm = llm
        self.tool_executor = tool_executor
        self.tool_registry = tool_registry
        self.max_iterations = max_iterations

    def run(self, system_prompt: str, user_input: str):
        response = self.llm.create_response(
            instructions=system_prompt,
            user_input=user_input,
            tools=self.tool_registry.get_definitions(),
            store=True
        )

        for i in range(self.max_iterations):
            print(f'========= Agent iteration {i + 1} =========')
            tool_outputs = []

            for item in response.output:
                print('TYPE', item.type)
                if item.type == 'function_call':
                    print('Tool Name:', item.name)
                    print('Arguments:', item.arguments)
                    arguments = json.loads(item.arguments)
                    result = self.tool_executor.execute(item.name, arguments)
                    print("Tool result:")
                    print(result)
                    tool_outputs.append({
                        'type': 'function_call_output',
                        'call_id': item.call_id,
                        'output': json.dumps(result),
                    })

            # No tool calls means we are done
            if not tool_outputs:
                print("============ Agent finished =============")
                return response.output_text

            # Send ALL tool results back
            response = self.llm.create_response(
                previous_response_id=response.id,
                user_input=tool_outputs,
                tools=self.tool_registry.get_definitions(),
            )
        raise RuntimeError('Agent exceeded maximum number of iterations')