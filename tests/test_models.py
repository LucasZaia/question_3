from semantic_search.models import SearchResult


def test_search_result_exposes_content_score_and_source() -> None:
    result = SearchResult(
        id="document-0",
        content="Conteúdo relevante.",
        score=0.91,
        source="guide.md",
    )

    assert result.id == "document-0"
    assert result.content == "Conteúdo relevante."
    assert result.score == 0.91
    assert result.source == "guide.md"
