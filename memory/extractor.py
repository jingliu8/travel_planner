from typing import Optional
from models.memory import MemoryOperationList
from memory.prompts import MEMORY_EXTRACTION_PROMPT

class MemoryExtractor:
    """Extracts memory operations from user input using LLM."""

    def __init__(self, llm):
        """
        Initialize the memory extractor.
        
        Args:
            llm: LLM client for processing user input
            
        Raises:
            ValueError: If llm is None
        """
        if not llm:
            raise ValueError("llm cannot be None")
        
        self.llm = llm

    def extract(self, user_input: str) -> MemoryOperationList:
        """
        Extract memory operations from user input.
        
        Analyzes the user message and returns memory operations
        (add, update, delete) based on the input.
        
        Args:
            user_input: User's input message
            
        Returns:
            MemoryOperationList with extracted operations
        """
        if not user_input:
            raise ValueError("user_input cannot be empty")
        
        try:
            response = self.llm.create_response(
                instructions=MEMORY_EXTRACTION_PROMPT,
                input=user_input
            )
        except Exception as e:
            raise Exception(f"Failed to extract memories from input: {str(e)}")

        return MemoryOperationList.model_validate_json(response.output_text)
