from pathlib import Path
from typing import Any

from semantic_search.evaluation.dataset import load_evaluation_cases
from semantic_search.evaluation.evaluator import EvaluationReport, evaluate_search


class EvaluationService:
    def __init__(self, search_service: Any) -> None:
        self.search_service = search_service

    def evaluate(self, dataset_path: Path, limit: int) -> EvaluationReport:
        cases = load_evaluation_cases(dataset_path)
        return evaluate_search(self.search_service.search, cases, limit)
