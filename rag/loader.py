from pathlib import Path
from models import Document

class DocumentLoader:
    def __init__(self, knowledge_dir: str):
        self.knowledge_dir = Path(knowledge_dir)

    def load_documents(self) -> list[Document]:
        documents = []

        for path in self.knowledge_dir.glob("*.txt"):
            content = path.read_text(encoding="utf-8")
            document = Document(
                source=path.name,
                content=content,
            )
            documents.append(document)

        return documents