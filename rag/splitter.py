from models.rag import Chunk, Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextSplitter:
    def __init__(self, chunk_size: int=500, chunk_overlap: int=100):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ],
        )

    def split_documents(self, documents: list[Document]) -> list[Chunk]:
        chunks = []

        for document in documents:
            split_texts = self.splitter.split_text(document.content)
            for i, text in enumerate(split_texts):
                chunk = Chunk(
                    id=f'{document.source}_{i}',
                    source=document.source,
                    content=text,
                )
                chunks.append(chunk)

        return chunks


