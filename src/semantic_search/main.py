import logging
import sys
from pathlib import Path

from semantic_search.cli import run_cli
from semantic_search.config import get_settings
from semantic_search.embeddings.openai import create_embeddings
from semantic_search.evaluation.service import EvaluationService
from semantic_search.loaders.text_loader import TextDocumentLoader
from semantic_search.processors.text_splitter import DocumentChunker
from semantic_search.reranking.openai_reranker import OpenAIReranker
from semantic_search.services.ingestion_service import IngestionService
from semantic_search.services.search_service import SearchService
from semantic_search.vector_store.pinecone_store import PineconeVectorStoreFactory


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    logging.getLogger(__name__).info("application started command=%s", arguments[0] if arguments else "none")
    embeddings = create_embeddings(settings)
    vector_store = PineconeVectorStoreFactory(settings, embeddings).create()
    ingestion_service = IngestionService(
        TextDocumentLoader(),
        DocumentChunker(settings.chunk_size, settings.chunk_overlap),
        vector_store,
    )
    reranker = None
    if arguments and arguments[0] in {"search", "eval"}:
        reranker = OpenAIReranker(settings.openai_api_key, settings.reranker_model)
    search_service = SearchService(
        vector_store,
        reranker=reranker,
        candidate_limit=settings.reranker_candidates,
    )
    evaluation_service = EvaluationService(search_service)
    return run_cli(arguments, ingestion_service, search_service, evaluation_service)


if __name__ == "__main__":
    raise SystemExit(main())
