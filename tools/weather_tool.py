import requests


class WeatherTool:

    name = "get_weather"

    description = """
    Get current weather information for a city.
    Use this when the user asks about weather,
    temperature, wind, or current conditions.
    """

    def __init__(self):

        self.geo_url = ("https://geocoding-api.open-meteo.com/v1/search")
        self.weather_url = ("https://api.open-meteo.com/v1/forecast")


    def definition(self):
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string"
                    }
                },
                "required": [
                    "city"
                ],
                "additionalProperties": False
            }
        }


    def execute(self, city: str):

        location = self.get_coordinates(city)

        weather = self.get_current_weather(
            location["latitude"],
            location["longitude"]
        )

        return {
            "city": location["name"],
            "temperature": weather["temperature"],
            "wind_speed": weather["windspeed"],
            "weather_code": weather["weathercode"]
        }


    def get_coordinates(self, city: str):

        city = city.split(",")[0].strip()

        response = requests.get(
            self.geo_url,
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


    def get_current_weather(
        self,
        latitude: float,
        longitude: float
    ):

        response = requests.get(
            self.weather_url,
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