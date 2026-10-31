import logging
import hashlib
from pathlib import Path
from typing import Any


logger = logging.getLogger(__name__)


class IngestionService:
    def __init__(self, loader: Any, chunker: Any, vector_store: Any) -> None:
        self.loader = loader
        self.chunker = chunker
        self.vector_store = vector_store

    def ingest(self, directory: Path) -> int:
        logger.info("ingestion started directory=%s", directory)
        documents = self.loader.load(directory)
        chunks = self.chunker.split(documents)
        if not chunks:
            logger.info("ingestion completed chunks=0")
            return 0

        ids: list[str] = []
        for chunk in chunks:
            source = str(chunk.metadata.get("source", "unknown"))
            chunk_number = str(chunk.metadata.get("chunk", 0))
            identity = f"{source}:{chunk_number}:{chunk.page_content}"
            vector_id = hashlib.sha256(identity.encode("utf-8")).hexdigest()
            chunk.metadata = {**chunk.metadata, "id": vector_id}
            ids.append(vector_id)

        self.vector_store.add_documents(documents=chunks, ids=ids)
        logger.info("ingestion completed chunks=%s", len(chunks))
        return len(chunks)
