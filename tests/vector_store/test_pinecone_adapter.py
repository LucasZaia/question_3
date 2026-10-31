import pytest
from langchain_core.documents import Document

from semantic_search.vector_store.pinecone_store import PineconeVectorStoreAdapter


class FakeLangChainVectorStore:
    def similarity_search_with_score(self, query: str, k: int):
        assert query == "arquitetura da informação"
        assert k == 3
        return [(Document(page_content="conteúdo relevante"), 0.91)]


def test_query_delegates_to_langchain_vector_store() -> None:
    adapter = PineconeVectorStoreAdapter(FakeLangChainVectorStore())

    matches = adapter.query("arquitetura da informação", limit=3)

    assert matches[0][0].page_content == "conteúdo relevante"
    assert matches[0][1] == 0.91


@pytest.mark.parametrize("query, limit", [("", 3), ("consulta", 0)])
def test_query_rejects_invalid_arguments(query: str, limit: int) -> None:
    adapter = PineconeVectorStoreAdapter(FakeLangChainVectorStore())

    with pytest.raises(ValueError):
        adapter.query(query, limit)
