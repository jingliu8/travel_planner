from typing import Any, Callable, Dict, Optional
from functools import wraps

from tools.tool_executor_improve import ToolExecutionError

class ToolRegistry:
    """Central registry for tools with decorator-based auto-registration."""

    _instance: Optional["ToolRegistry"] = None
    _tools: Dict[str, Dict[str, Any]] = {}

    def __new__(cls):
        """Implement singleton pattern for the registry."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the registry (called once due to singleton)."""
        pass

    def register(self, name: str, func: Callable, definition: Dict[str, Any]) -> None:
        """Manually register a tool."""
        self._tools[name] = {"function": func, "definition": definition}

    def get_definitions(self) -> list:
        """Get all tool definitions."""
        return [tool["definition"] for tool in self._tools.values()]

    def execute(self, name: str, args: Dict[str, Any]) -> Any:
        """Execute a registered tool."""
        if name not in self._tools:
            raise ToolExecutionError(f"Tool '{name}' not registered")

        func = self._tools[name]["function"]
        return func(**args)


def tool(definition: Dict[str, Any]) -> Callable:
    """Decorator to automatically register a tool.
    
    Usage:
        @tool(weather_tool)
        def get_weather(city: str):
            ...
    
    Args:
        definition: The tool definition dict (from tool_definitions.py)
    
    Returns:
        A decorator that registers the function and returns it unchanged.
    """
    def decorator(func: Callable) -> Callable:
        registry = ToolRegistry()
        tool_name = definition.get("name", str(func.__name__))
        registry.register(tool_name, func, definition)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    return decorator