import requests
from tools.tool_registry import tool
from tools.tool_definitions import weather_tool

geo_url = "https://geocoding-api.open-meteo.com/v1/search"
weather_url = "https://api.open-meteo.com/v1/forecast"

def get_coordinates(city: str):
    city = city.split(',')[0].strip()
    response = requests.get(
        geo_url,
        params={
            "name": city,
            "count": 1
        },
        timeout=5
    )

    response.raise_for_status()

    data = response.json()

    if "results" not in data:
        raise ValueError(
            f"Cannot find location: {city}"
        )

    location = data["results"][0]

    return {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "name": location["name"]
    }

def get_current_weather(latitude: float, longitude: float):
    response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True
        },
        timeout=5
    )
    response.raise_for_status()
    data = response.json()
    return data["current_weather"]


@tool(weather_tool)
def get_weather(city: str):
    location = get_coordinates(city)
    weather = get_current_weather(
        location["latitude"],
        location["longitude"]
    )
    return {
        "city": location["name"],
        "temperature": weather["temperature"],
        "wind_speed": weather["windspeed"],
        "weather_code": weather["weathercode"]
    }