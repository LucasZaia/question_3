import logging
import json
from typing import Any

from openai import OpenAI

from semantic_search.models import SearchResult


logger = logging.getLogger(__name__)


class OpenAIReranker:
    def __init__(self, api_key: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def rerank(
        self,
        query: str,
        candidates: list[SearchResult],
        limit: int,
    ) -> list[SearchResult]:
        if not candidates:
            return []
        logger.info("OpenAI reranking started candidates=%s limit=%s", len(candidates), limit)
        payload = [
            {"id": result.id, "content": result.content}
            for result in candidates
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Rank the documents by relevance to the query. "
                        "Return only JSON in the format {\"ranking\": [\"id\", ...]}. "
                        "Include each valid document ID at most once."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {"query": query, "documents": payload},
                        ensure_ascii=False,
                    ),
                },
            ],
        )
        content = response.choices[0].message.content or "{}"
        ranking = json.loads(content).get("ranking", [])
        by_id = {result.id: result for result in candidates}
        ordered = [by_id[result_id] for result_id in ranking if result_id in by_id]
        ordered_ids = {result.id for result in ordered}
        ordered.extend(result for result in candidates if result.id not in ordered_ids)
        ranked = ordered[:limit]
        logger.info("OpenAI reranking completed results=%s", len(ranked))
        return ranked
