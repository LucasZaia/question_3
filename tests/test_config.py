import pytest
from pydantic import ValidationError

from semantic_search.config import Settings


def test_settings_require_api_keys() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_settings_use_transformer_and_pinecone_defaults() -> None:
    settings = Settings(
        _env_file=None,
        openai_api_key="openai-test-key",
        pinecone_api_key="pinecone-test-key",
    )

    assert settings.embedding_model == "text-embedding-3-small"
    assert settings.embedding_dimension == 1536
    assert settings.pinecone_index_name == "semantic-search-openai"
    assert settings.reranker_model == "gpt-5-mini"
    assert settings.reranker_candidates == 10
    assert settings.chunk_size == 800
    assert settings.chunk_overlap == 120
