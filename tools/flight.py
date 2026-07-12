from datetime import datetime


def search_flight(
        origin: str,
        destination: str,
        date: str
):
    """
    Search available flights.
    """

    return {
        "origin": origin,
        "destination": destination,
        "date": date,
        "flights": [
            {
                "airline": "Delta",
                "departure": "08:30",
                "arrival": "11:45",
                "price": "$250"
            },
            {
                "airline": "United",
                "departure": "14:20",
                "arrival": "17:35",
                "price": "$220"
            }
        ]
    }
