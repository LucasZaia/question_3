from collections.abc import Callable, Iterable
from dataclasses import dataclass

from semantic_search.models import SearchResult


@dataclass(frozen=True)
class EvaluationCase:
    query: str
    relevant_sources: set[str]


@dataclass(frozen=True)
class EvaluationReport:
    query_count: int
    limit: int
    hit_rate: float
    mrr: float
    precision_at_k: float


def evaluate_search(
    search: Callable[[str, int], list[SearchResult]],
    cases: Iterable[EvaluationCase],
    limit: int,
) -> EvaluationReport:
    if limit <= 0:
        raise ValueError("Evaluation limit must be greater than zero")

    cases_list = list(cases)
    if not cases_list:
        raise ValueError("Evaluation dataset cannot be empty")

    hits = 0
    reciprocal_ranks = 0.0
    precisions = 0.0
    for case in cases_list:
        results = search(case.query, limit)
        relevant_positions = [
            position
            for position, result in enumerate(results[:limit])
            if result.source in case.relevant_sources
        ]
        if relevant_positions:
            hits += 1
            reciprocal_ranks += 1 / (relevant_positions[0] + 1)
        relevant_count = sum(
            result.source in case.relevant_sources for result in results[:limit]
        )
        precisions += relevant_count / limit

    query_count = len(cases_list)
    return EvaluationReport(
        query_count=query_count,
        limit=limit,
        hit_rate=hits / query_count,
        mrr=reciprocal_ranks / query_count,
        precision_at_k=precisions / query_count,
    )
