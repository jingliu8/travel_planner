import requests
from typing import Dict, Any

class WeatherTool:
    """Tool for retrieving current weather information for a given city."""

    name = "get_weather"

    description = """
    Get current weather information for a city.
    Use this when the user asks about weather,
    temperature, wind, or current conditions.
    """

    DEFAULT_GEO_TIMEOUT = 5
    DEFAULT_WEATHER_TIMEOUT = 5
    DEFAULT_LOCATION_COUNT = 1

    def __init__(self):
        """Initialize the weather tool with API endpoints."""
        self.geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"

    def definition(self) -> Dict[str, Any]:
        """
        Get the tool definition for the agent.
        
        Returns:
            Tool definition dictionary
        """
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name to get weather for"
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }

    def execute(self, city: str) -> Dict[str, Any]:
        """
        Execute the weather tool to get weather information.
        
        Args:
            city: City name
            
        Returns:
            Dictionary with city, temperature, wind_speed, and weather_code
            
        Raises:
            ValueError: If city is empty
            Exception: If API calls fail
        """
        if not city or not city.strip():
            raise ValueError("city cannot be empty")
        
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

    def get_coordinates(self, city: str) -> Dict[str, Any]:
        """
        Get latitude and longitude for a city using geocoding API.
        
        Args:
            city: City name
            
        Returns:
            Dictionary with latitude, longitude, and name
            
        Raises:
            ValueError: If city not found or API error
        """
        if not city or not city.strip():
            raise ValueError("city cannot be empty")
        
        city_name = city.split(",")[0].strip()

        try:
            response = requests.get(
                self.geo_url,
                params={
                    "name": city_name,
                    "count": self.DEFAULT_LOCATION_COUNT
                },
                timeout=self.DEFAULT_GEO_TIMEOUT
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(f"Failed to get coordinates for '{city_name}': {str(e)}")

        data = response.json()

        if "results" not in data or not data["results"]:
            raise ValueError(f"City not found: {city_name}")

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
    ) -> Dict[str, Any]:
        """
        Get current weather information for coordinates.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dictionary with temperature, windspeed, and weathercode
            
        Raises:
            ValueError: If coordinates invalid or API error
        """
        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            raise ValueError("latitude and longitude must be numbers")

        try:
            response = requests.get(
                self.weather_url,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current_weather": True
                },
                timeout=self.DEFAULT_WEATHER_TIMEOUT
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(f"Failed to get weather data: {str(e)}")
        
        data = response.json()
        
        if "current_weather" not in data:
            raise ValueError("Invalid weather response from API")
        
        return data["current_weather"]