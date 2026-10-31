import json
from pathlib import Path

from semantic_search.evaluation.evaluator import EvaluationCase


def load_evaluation_cases(path: Path) -> list[EvaluationCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        EvaluationCase(
            query=item["query"],
            relevant_sources=set(item["relevant_sources"]),
        )
        for item in payload
    ]
