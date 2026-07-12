from tools.tool_executor_improve import ToolExecutionError

class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, name, func, definition):
        self.tools[name] = {"function": func, "definition": definition}

    def get_definitions(self):
        return [tool["definition"] for tool in self.tools.values()]

    def execute(self, name, args):
        if name not in self.tools:
            raise ToolExecutionError(f"Tool {name} not registered")

        func = self.tools[name]["function"]
        return func(*args)