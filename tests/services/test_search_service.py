from langchain_core.documents import Document

from semantic_search.services.search_service import SearchService


class FakeVectorStore:
    def query(self, query: str, limit: int):
        assert query == "comandos Linux"
        assert limit == 2
        return [
            (
                Document(
                    page_content="Como listar arquivos.",
                    metadata={"source": "linux.md", "chunk": 0},
                ),
                0.93,
            )
        ]


def test_search_maps_vector_store_matches_to_search_results(caplog) -> None:
    caplog.set_level("INFO")
    results = SearchService(FakeVectorStore()).search("comandos Linux", limit=2)

    assert len(results) == 1
    assert results[0].content == "Como listar arquivos."
    assert results[0].score == 0.93
    assert results[0].source == "linux.md"
    assert "semantic search started" in caplog.text
    assert "semantic search completed" in caplog.text
