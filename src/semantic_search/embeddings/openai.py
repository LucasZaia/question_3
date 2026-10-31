import logging
from collections.abc import Sequence
from typing import Any

from openai import OpenAI

from semantic_search.config import Settings


logger = logging.getLogger(__name__)


class OpenAIEmbeddingProvider:
    def __init__(self, api_key: str, model: str) -> None:
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        logger.info("creating embeddings model=%s documents=%s", self.model, len(texts))
        response = self.client.embeddings.create(
            input=list(texts),
            model=self.model,
        )
        vectors = [item.embedding for item in response.data]
        logger.info("embeddings created vectors=%s", len(vectors))
        return vectors

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]


def create_embeddings(settings: Settings) -> OpenAIEmbeddingProvider:
    return OpenAIEmbeddingProvider(settings.openai_api_key, settings.embedding_model)
