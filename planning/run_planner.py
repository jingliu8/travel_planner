from llm import LLMClient
from planning.planner import Planner


llm = LLMClient()

planner = Planner(llm)

plan = planner.create_plan(
    "Plan a 4 day hiking trip to Asheville"
)


print(plan)