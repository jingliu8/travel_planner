class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, tool):
        self.tools[tool.name] = tool

    def get(self, name):
        return self.tools[name]

    def get_definitions(self):
        return list(tool.definition() for tool in self.tools.values())