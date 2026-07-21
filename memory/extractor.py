from models.memory import MemoryOperationList
from memory.prompts import MEMORY_EXTRACTION_PROMPT

class MemoryExtractor:

    def __init__(self, llm):
        self.llm = llm

    def extract(self, user_input: str) -> MemoryOperationList:
        response = self.llm.create_response(
            instructions=MEMORY_EXTRACTION_PROMPT,
            input=user_input
        )
        return MemoryOperationList.model_validate_json(response.output_text)