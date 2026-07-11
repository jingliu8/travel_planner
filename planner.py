import json
from llm import LLMClient
from prompts import TRAVEL_PLANNER_SYSTEM_PROMPT, TRAVEL_USER_PROMPT
from models import TravelPlan, TravelRequest
from rag.retriever import Retriever
from tools.tool_executor import ToolExecutor
from tools.tool_definitions import weather_tool, flight_tool

max_iteration_tool_calling = 5

class TravelPlanner:
    def __init__(self, llm_client: LLMClient, retriever: Retriever) -> None:
        self.llm = llm_client
        self.retriever = retriever

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
        response = self.llm.generate(
            system_prompt=TRAVEL_PLANNER_SYSTEM_PROMPT,
            user_input=user_input,
        )
        return TravelPlan.model_validate_json(response)


class TravelPlannerWithTools:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm = llm_client
        self.tool_executor = ToolExecutor()

    def generate_with_tools(self, user_input: str):

        response = self.llm.generate_with_tools(
            system_prompt="""
            You are a travel assistant.

            Use tools whenever they help answer the user's question.
            """,
            user_input=user_input,
            tools=[
                weather_tool,
                flight_tool,
            ]
        )
        for i in range(max_iteration_tool_calling):
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
                return response.output_text

            # Send ALL tool results back
            response = self.llm.submit_tool_results(
                previous_response_id=response.id,
                tool_outputs=tool_outputs
            )