import logging
from collections.abc import Callable
from typing import Any

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

from semantic_search.config import Settings


logger = logging.getLogger(__name__)


class PineconeVectorStoreAdapter:
    """Application-facing adapter around LangChain's Pinecone vector store."""

    def __init__(self, vector_store: Any) -> None:
        self.vector_store = vector_store

    def add_documents(self, *, documents: list[Any], ids: list[str]) -> Any:
        logger.info("upserting documents into Pinecone count=%s", len(documents))
        return self.vector_store.add_documents(documents=documents, ids=ids)

    def query(self, query: str, limit: int) -> list[tuple[Any, float]]:
        """Return the nearest documents and their vector similarity scores."""
        if not query.strip():
            raise ValueError("Vector store query cannot be empty")
        if limit <= 0:
            raise ValueError("Vector store query limit must be greater than zero")

        logger.info("querying Pinecone vector store limit=%s", limit)
        return self.vector_store.similarity_search_with_score(query, k=limit)


class PineconeVectorStoreFactory:
    def __init__(
        self,
        settings: Settings,
        embeddings: Any,
        client_factory: Callable[..., Any] = Pinecone,
        vector_store_factory: Callable[..., Any] = PineconeVectorStore,
    ) -> None:
        self.settings = settings
        self.embeddings = embeddings
        self.client_factory = client_factory
        self.vector_store_factory = vector_store_factory

    def create(self) -> Any:
        logger.info("connecting to Pinecone index=%s", self.settings.pinecone_index_name)
        client = self.client_factory(api_key=self.settings.pinecone_api_key)
        index_name = self.settings.pinecone_index_name

        if not client.has_index(index_name):
            logger.info("creating Pinecone index=%s", index_name)
            client.create_index(
                name=index_name,
                dimension=self.settings.embedding_dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=self.settings.pinecone_cloud,
                    region=self.settings.pinecone_region,
                ),
            )

        index = client.Index(index_name)
        logger.info("Pinecone vector store ready namespace=%s", self.settings.pinecone_namespace)
        vector_store = self.vector_store_factory(
            index=index,
            embedding=self.embeddings,
            namespace=self.settings.pinecone_namespace,
        )
        return PineconeVectorStoreAdapter(vector_store)
