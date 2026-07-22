from typing import Any, Dict, List

class SearchKnowledgeTool:
    """Tool for searching the knowledge base using RAG retriever."""

    name = "search_knowledge"

    description = """
    Search the internal knowledge base.
    Use this when you need information from stored documents.
    """

    def __init__(self, retriever):
        """
        Initialize the search knowledge tool.
        
        Args:
            retriever: Retriever object with retrieve method
            
        Raises:
            ValueError: If retriever is None or doesn't have retrieve method
        """
        if not retriever:
            raise ValueError("retriever cannot be None")
        
        if not hasattr(retriever, 'retrieve'):
            raise ValueError("retriever must have a 'retrieve' method")
        
        self.retriever = retriever

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
                    "query": {
                        "type": "string",
                        "description": "Search query for the knowledge base"
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }

    def execute(self, query: str) -> List[Any]:
        """
        Execute the search knowledge tool.
        
        Args:
            query: Search query string
            
        Returns:
            List of relevant chunks from the knowledge base
            
        Raises:
            ValueError: If query is empty
        """
        if not query or not query.strip():
            raise ValueError("query cannot be empty")
        
        return self.retriever.retrieve(query)

