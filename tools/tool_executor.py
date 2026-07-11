from tools.weather import get_weather
from tools.flight import search_flight

class ToolExecutor:
    def execute(self, tool_name: str, arguments: dict):
        if tool_name == "get_weather":
            return get_weather(**arguments)

        if tool_name == "search_flight":
            return search_flight(**arguments)

        raise ValueError(
            f'Tool "{tool_name}" is not supported.'
        )