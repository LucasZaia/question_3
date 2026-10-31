import json
from pathlib import Path

from semantic_search.evaluation.dataset import load_evaluation_cases


def test_load_evaluation_cases_from_json(tmp_path: Path) -> None:
    dataset = tmp_path / "queries.json"
    dataset.write_text(
        json.dumps(
            [
                {"query": "memória Linux", "relevant_sources": ["linux.md"]}
            ]
        ),
        encoding="utf-8",
    )

    cases = load_evaluation_cases(dataset)

    assert cases[0].query == "memória Linux"
    assert cases[0].relevant_sources == {"linux.md"}
