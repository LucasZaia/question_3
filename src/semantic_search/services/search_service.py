import logging
from typing import Any

from semantic_search.models import SearchResult


logger = logging.getLogger(__name__)


class SearchService:
    def __init__(
        self,
        vector_store: Any,
        reranker: Any | None = None,
        candidate_multiplier: int = 3,
        candidate_limit: int | None = None,
    ) -> None:
        self.vector_store = vector_store
        self.reranker = reranker
        self.candidate_multiplier = candidate_multiplier
        self.candidate_limit = candidate_limit

    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        normalized_query = query.strip()
        if not normalized_query:
            raise ValueError("Search query cannot be empty")
        if limit <= 0:
            raise ValueError("Search limit must be greater than zero")

        logger.info("semantic search started query=%r limit=%s", normalized_query, limit)

        candidate_limit = (
            max(
                self.candidate_limit or limit * self.candidate_multiplier,
                limit,
            )
            if self.reranker is not None
            else limit
        )
        matches = self.vector_store.query(
            normalized_query,
            limit=candidate_limit,
        )
        results: list[SearchResult] = []
        for document, score in matches:
            metadata = document.metadata
            source = str(metadata.get("source", "unknown"))
            result_id = str(metadata.get("id", f"{source}:{metadata.get('chunk', 0)}"))
            results.append(
                SearchResult(
                    id=result_id,
                    content=document.page_content,
                    score=float(score),
                    source=source,
                )
            )
        if self.reranker is not None:
            logger.info("reranking candidates=%s", len(results))
            results = self.reranker.rerank(normalized_query, results, limit)
        logger.info("semantic search completed results=%s", len(results))
        return results
