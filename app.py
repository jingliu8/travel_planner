from llm import LLMClient
from planner import TravelPlanner


def main():

    llm = LLMClient()

    planner = TravelPlanner(
        llm_client=llm
    )

    request = """
    Plan a 4-day trip to Asheville, NC.

    I like:
    - hiking
    - nature
    - scenic drives
    - local food

    I do not like:
    - museums
    - crowded attractions
    """

    result = planner.generate_itinerary(request)

    print(result)


if __name__ == "__main__":
    main()