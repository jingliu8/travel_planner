from llm import LLMClient
from planner import TravelPlanner
from models import TravelRequest


def main():
    # 1. Create LLM client
    llm = LLMClient()

    # 2. Inject llm client into planner
    planner = TravelPlanner(llm_client=llm)

    # 3. Create user request
    request = TravelRequest(
        destination='Asheville',
        days=4,
        interests=['hiking', 'nature', 'hot springs']
    )
    # 4. Generate itinerary
    plan = planner.generate_itinerary(request)

    # 5. Consume TravelPlan object
    print("=" * 50)
    print(f"Destination: {plan.destination}")
    print("=" * 50)

    for day_plan in plan.days:
        print(f"\nDay {day_plan.day}")

        print("Activities:")
        for activity in day_plan.activities:
            print(f"  - {activity}")

        print("Restaurants:")
        for restaurant in day_plan.restaurants:
            print(f"  - {restaurant}")


if __name__ == "__main__":
    main()