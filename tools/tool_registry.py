from typing import Optional, Dict, List, Any

class ToolRegistry:
    """Registry for managing and retrieving tools used by the agent."""

    def __init__(self):
        """Initialize the tool registry."""
        self.tools: Dict[str, Any] = {}

    def register(self, tool) -> None:
        """
        Register a new tool.
        
        Args:
            tool: Tool object with name attribute
            
        Raises:
            ValueError: If tool has no name attribute or if name already exists
        """
        if not hasattr(tool, 'name'):
            raise ValueError("Tool must have a 'name' attribute")
        
        if tool.name in self.tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")
        
        self.tools[tool.name] = tool

    def unregister(self, name: str) -> None:
        """
        Unregister a tool.
        
        Args:
            name: Tool name
            
        Raises:
            ValueError: If tool not found
        """
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found")
        
        del self.tools[name]

    def get(self, name: str) -> Any:
        """
        Get a tool by name.
        
        Args:
            name: Tool name
            
        Returns:
            Tool object
            
        Raises:
            ValueError: If tool not found
        """
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found")
        
        return self.tools[name]

    def exists(self, name: str) -> bool:
        """
        Check if a tool is registered.
        
        Args:
            name: Tool name
            
        Returns:
            True if tool exists, False otherwise
        """
        return name in self.tools

    def get_definitions(self) -> List[Dict[str, Any]]:
        """
        Get definitions of all registered tools.
        
        Returns:
            List of tool definitions
        """
        return [tool.definition() for tool in self.tools.values()]

    def list_tools(self) -> List[str]:
        """
        List all registered tool names.
        
        Returns:
            List of tool names
        """
        return list(self.tools.keys())

    def get_tool_count(self) -> int:
        """
        Get the number of registered tools.
        
        Returns:
            Number of tools
        """
        return len(self.tools)