from langchain_core.documents import Document

from semantic_search.processors.text_splitter import DocumentChunker


def test_chunker_splits_documents_and_preserves_source_metadata() -> None:
    document = Document(
        page_content="um dois três quatro cinco seis sete oito nove dez",
        metadata={"source": "guide.md"},
    )

    chunks = DocumentChunker(chunk_size=20, chunk_overlap=5).split([document])

    assert len(chunks) > 1
    assert all(chunk.metadata["source"] == "guide.md" for chunk in chunks)
    assert all(chunk.metadata["chunk"] == index for index, chunk in enumerate(chunks))


def test_chunker_rejects_overlap_equal_to_chunk_size() -> None:
    try:
        DocumentChunker(chunk_size=20, chunk_overlap=20)
    except ValueError as exc:
        assert "chunk_overlap" in str(exc)
    else:
        raise AssertionError("Expected invalid overlap to raise ValueError")
