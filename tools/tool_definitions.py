weather_tool = {
    "type": "function",
    "name": "get_weather",
    "description": "Get weather information for a city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city name"
            }
        },
        "required": [
            "city"
        ]
    }
}

flight_tool = {
    "type": "function",
    "name": "search_flight",
    "description": """
    Search flights between two cities on a specific date.
    Use this tool when the user asks about flights,
    airfare, airlines, departure time, or travel options.
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "origin": {
                "type": "string",
                "description": "Departure city"
            },
            "destination": {
                "type": "string",
                "description": "Arrival city"
            },
            "date": {
                "type": "string",
                "description": "Travel date in YYYY-MM-DD format"
            }
        },
        "required": [
            "origin",
            "destination",
            "date"
        ],
        "additionalProperties": False
    }
}

# other_tools...