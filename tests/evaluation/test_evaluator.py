from semantic_search.evaluation.evaluator import EvaluationCase, evaluate_search
from semantic_search.models import SearchResult


def test_evaluator_calculates_hit_rate_mrr_and_precision_at_k() -> None:
    cases = [
        EvaluationCase(query="memória Linux", relevant_sources={"linux.md"}),
        EvaluationCase(query="funções Python", relevant_sources={"python.md"}),
    ]

    def search(query: str, limit: int):
        if query == "memória Linux":
            return [
                SearchResult(id="1", content="Linux", score=0.9, source="linux.md"),
                SearchResult(id="2", content="Docker", score=0.8, source="docker.md"),
            ]
        return [
            SearchResult(id="3", content="Docker", score=0.9, source="docker.md"),
            SearchResult(id="4", content="Python", score=0.8, source="python.md"),
        ]

    report = evaluate_search(search, cases, limit=2)

    assert report.query_count == 2
    assert report.hit_rate == 1.0
    assert report.mrr == 0.75
    assert report.precision_at_k == 0.5


def test_evaluator_handles_queries_without_relevant_results() -> None:
    case = EvaluationCase(query="cloud", relevant_sources={"cloud.md"})

    report = evaluate_search(
        lambda query, limit: [
            SearchResult(id="1", content="Linux", score=0.4, source="linux.md")
        ],
        [case],
        limit=3,
    )

    assert report.hit_rate == 0.0
    assert report.mrr == 0.0
    assert report.precision_at_k == 0.0
