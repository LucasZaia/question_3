from pathlib import Path

from semantic_search.cli import run_cli
from semantic_search.models import SearchResult


class FakeIngestionService:
    def ingest(self, directory: Path) -> int:
        assert directory == Path("data/documents")
        return 3


class FakeSearchService:
    def search(self, query: str, limit: int):
        assert query == "comandos Linux"
        assert limit == 2
        return [
            SearchResult(
                id="result-1",
                content="Use o comando ls.",
                score=0.9,
                source="linux.md",
            )
        ]


class FakeEvaluationService:
    def evaluate(self, dataset, limit):
        assert dataset == Path("data/evaluation/queries.json")
        assert limit == 3
        return type(
            "Report",
            (),
            {
                "query_count": 4,
                "limit": 3,
                "hit_rate": 0.75,
                "mrr": 0.625,
                "precision_at_k": 0.5,
            },
        )()


def test_cli_ingest_prints_indexed_chunk_count() -> None:
    output: list[str] = []

    exit_code = run_cli(
        ["ingest", "--directory", "data/documents"],
        FakeIngestionService(),
        FakeSearchService(),
        output_fn=output.append,
    )

    assert exit_code == 0
    assert output == ["3 chunks indexed."]


def test_cli_search_prints_ranked_results() -> None:
    output: list[str] = []

    exit_code = run_cli(
        ["search", "comandos Linux", "--limit", "2"],
        FakeIngestionService(),
        FakeSearchService(),
        output_fn=output.append,
    )

    assert exit_code == 0
    assert "[rank=1 score=0.9000] linux.md: Use o comando ls." in output


def test_cli_eval_prints_relevance_metrics() -> None:
    output: list[str] = []

    exit_code = run_cli(
        ["eval", "--limit", "3"],
        FakeIngestionService(),
        FakeSearchService(),
        FakeEvaluationService(),
        output_fn=output.append,
    )

    assert exit_code == 0
    assert "Taxa de acerto@3: 0.7500" in output
    assert "Reciprocidade média do ranking@3 (MRR): 0.6250" in output
    assert "Precisão@3: 0.5000" in output
