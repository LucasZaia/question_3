import logging
from pathlib import Path

from langchain_core.documents import Document


logger = logging.getLogger(__name__)


class TextDocumentLoader:
    def load(self, directory: Path) -> list[Document]:
        if not directory.exists():
            raise FileNotFoundError(f"Documents directory not found: {directory}")
        if not directory.is_dir():
            raise NotADirectoryError(f"Documents path is not a directory: {directory}")

        documents: list[Document] = []
        for path in sorted(directory.glob("*.md")):
            content = path.read_text(encoding="utf-8").strip()
            if content:
                documents.append(Document(page_content=content, metadata={"source": path.name}))
        logger.info("documents loaded directory=%s count=%s", directory, len(documents))
        return documents
