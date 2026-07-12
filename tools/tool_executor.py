from typing import Any

from tools.tool_registry import ToolRegistry

class ToolExecutor():
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(self, tool_name: str, arguments: dict[str, Any]):
        return self.registry.execute(name=tool_name, args=arguments)