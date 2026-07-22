from typing import Any, Dict

from tools.tool_registry import ToolRegistry

class ToolExecutor:
    """Executor for running tools from the registry."""

    def __init__(self, registry: ToolRegistry):
        """
        Initialize the tool executor.
        
        Args:
            registry: ToolRegistry instance containing registered tools
            
        Raises:
            ValueError: If registry is None
        """
        if not registry:
            raise ValueError("registry cannot be None")
        
        self.registry = registry

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool with the given arguments.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Dictionary of arguments to pass to the tool
            
        Returns:
            Result from tool execution
            
        Raises:
            ValueError: If tool_name is empty or arguments is None
            Exception: Tool-specific exceptions
        """
        if not tool_name or not tool_name.strip():
            raise ValueError("tool_name cannot be empty")
        
        if arguments is None:
            raise ValueError("arguments cannot be None")
        
        if not isinstance(arguments, dict):
            raise ValueError("arguments must be a dictionary")
        
        tool = self.registry.get(tool_name)
        
        try:
            return tool.execute(**arguments)
        except TypeError as e:
            raise ValueError(f"Invalid arguments for tool '{tool_name}': {str(e)}")
        except Exception as e:
            raise Exception(f"Tool '{tool_name}' execution failed: {str(e)}")