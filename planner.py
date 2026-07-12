import json
from llm import LLMClient
from prompts import TRAVEL_PLANNER_SYSTEM_PROMPT, TRAVEL_USER_PROMPT
from models import TravelPlan, TravelRequest
from rag.retriever import Retriever
from tools.tool_executor import ToolExecutor
from tools.tool_registry import ToolRegistry


class TravelPlanner:

    def __init__(
        self,
        llm: LLMClient,
        retriever: Retriever,
        tool_executor: ToolExecutor,
        tool_registry: ToolRegistry,
        max_tool_iterations: int = 5,
    ):
        self.llm = llm
        self.retriever = retriever
        self.tool_executor = tool_executor
        self.tool_registry = tool_registry
        self.max_tool_iterations = max_tool_iterations

    def generate_itinerary(self, request: TravelRequest):
        query = f"""
                Destination: {request.destination}
                Days: {request.days}
                Interests: {', '.join(request.interests)}
                """
        chunks = self.retriever.retrieve(query)

        if not chunks:
            context = 'No relevant knowledge was found'
        else:
            context = '\n\n'.join(chunk.content for chunk in chunks)

        for chunk in chunks:
            print(chunk.source)
            print(chunk.content)
            print(chunk.similarity)
            print("-" * 40)

        user_input = TRAVEL_USER_PROMPT.format(
            context=context,
            destination=request.destination,
            days=request.days,
            interests=", ".join(request.interests)
        )
        response = self.run_agent(user_input)
        return TravelPlan.model_validate_json(response)


    def run_agent(self, user_input: str):

        response = self.llm.generate_with_tools(
            system_prompt=TRAVEL_PLANNER_SYSTEM_PROMPT,
            user_input=user_input,
            tools=self.tool_registry.get_definitions()
        )
        for i in range(self.max_tool_iterations):
            print(f'========= Agent iteration {i + 1} =========')

            tool_outputs = []

            for item in response.output:
                print('TYPE', item.type)

                if item.type == 'function_call':
                    print('Tool Name:', item.name)
                    print('Arguments:', item.arguments)
                    arguments = json.loads(item.arguments)
                    result = self.tool_executor.execute(
                        item.name,
                        arguments
                    )
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
            response = self.llm.submit_tool_results(
                previous_response_id=response.id,
                tool_outputs=tool_outputs
            )

        raise RuntimeError('Agent exceeded maximum number of iterations')