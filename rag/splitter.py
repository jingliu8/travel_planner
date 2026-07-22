from models.rag import Chunk, Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Optional

class TextSplitter:
    """Text splitter for RAG document chunking with configurable size and overlap."""
    
    DEFAULT_SEPARATORS = [
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
        separators: Optional[list[str]] = None
    ):
        """
        Initialize the text splitter.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of overlapping characters between chunks
            separators: Custom separators for text splitting
            
        Raises:
            ValueError: If chunk_size <= 0 or chunk_overlap >= chunk_size
        """
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators or self.DEFAULT_SEPARATORS,
        )

    def split_documents(self, documents: list[Document]) -> list[Chunk]:
        """
        Split documents into chunks.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of chunks
        """
        if not documents:
            raise ValueError("documents list cannot be empty")
        
        chunks = []
        
        for document in documents:
            if not document.content or not document.content.strip():
                continue
                
            split_texts = self.splitter.split_text(document.content)
            
            for i, text in enumerate(split_texts):
                chunk = Chunk(
                    id=f'{document.source}_{i}',
                    source=document.source,
                    content=text,
                )
                chunks.append(chunk)

        return chunks


