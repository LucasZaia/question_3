from pathlib import Path

from langchain_core.documents import Document

from semantic_search.services.ingestion_service import IngestionService


class FakeLoader:
    def load(self, directory: Path):
        return [Document(page_content="Conteúdo", metadata={"source": "guide.md"})]


class FakeChunker:
    def split(self, documents):
        return [
            Document(page_content="Primeiro", metadata={"source": "guide.md", "chunk": 0}),
            Document(page_content="Segundo", metadata={"source": "guide.md", "chunk": 1}),
        ]


class FakeVectorStore:
    def __init__(self) -> None:
        self.documents = None
        self.ids = None

    def add_documents(self, documents, ids):
        self.documents = documents
        self.ids = ids


def test_ingestion_adds_chunks_with_stable_ids(tmp_path: Path) -> None:
    vector_store = FakeVectorStore()
    service = IngestionService(FakeLoader(), FakeChunker(), vector_store)

    first = service.ingest(tmp_path)
    first_ids = vector_store.ids
    second = service.ingest(tmp_path)

    assert first == 2
    assert second == 2
    assert first_ids == vector_store.ids
    assert len(set(first_ids)) == 2
