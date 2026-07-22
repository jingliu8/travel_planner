class SearchKnowledgeTool:

    name = "search_knowledge"

    description = """
    Search the internal knowledge base.
    Use this when you need information from stored documents.
    """


    def __init__(self, retriever):
        self.retriever = retriever

    def definition(self):

        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    }
                },
                "required": [
                    "query"
                ],
                "additionalProperties": False
            }
        }

    def execute(self, query: str):
        return self.retriever.retrieve(query)

