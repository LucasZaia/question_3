import argparse
from collections.abc import Callable, Sequence
import os
from pathlib import Path
import sys
from typing import Any


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Semantic search with Transformer embeddings")
    commands = parser.add_subparsers(dest="command", required=True)

    ingest = commands.add_parser("ingest", help="Index local text documents in Pinecone")
    ingest.add_argument("--directory", type=Path, default=Path("data/documents"))

    search = commands.add_parser("search", help="Search indexed documents")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=5)

    evaluation = commands.add_parser("eval", help="Evaluate search relevance")
    evaluation.add_argument("--dataset", type=Path, default=Path("data/evaluation/queries.json"))
    evaluation.add_argument("--limit", type=int, default=5)
    return parser


def run_cli(
    argv: Sequence[str],
    ingestion_service: Any,
    search_service: Any,
    evaluation_service: Any = None,
    output_fn: Callable[[str], None] = print,
) -> int:
    args = build_parser().parse_args(argv)
    use_color = output_fn is print and sys.stdout.isatty() and "NO_COLOR" not in os.environ

    if args.command == "ingest":
        count = ingestion_service.ingest(args.directory)
        output_fn(f"{count} chunks indexed.")
        return 0

    if args.command == "eval":
        if evaluation_service is None:
            raise ValueError("Evaluation service is required for eval command")
        report = evaluation_service.evaluate(args.dataset, limit=args.limit)
        output_fn(f"Consultas avaliadas: {report.query_count}")
        output_fn(f"Taxa de acerto@{report.limit}: {report.hit_rate:.4f}")
        output_fn(
            f"Reciprocidade média do ranking@{report.limit} (MRR): "
            f"{report.mrr:.4f}"
        )
        output_fn(f"Precisão@{report.limit}: {report.precision_at_k:.4f}")
        return 0

    results = search_service.search(args.query, limit=args.limit)
    if not results:
        output_fn("No results found.")
        return 0
    for rank, result in enumerate(results, start=1):
        ranking_text = f"[rank={rank} score={result.score:.4f}]"
        if use_color:
            ranking_text = f"\033[96m{ranking_text}\033[0m"
        output_fn(
            f"{ranking_text} "
            f"{result.source}: {result.content}"
        )
    return 0
