from pathlib import Path

import pytest

from semantic_search.loaders.text_loader import TextDocumentLoader


def test_loader_reads_text_files_and_adds_source_metadata(tmp_path: Path) -> None:
    (tmp_path / "guide.md").write_text("Comando Linux útil.", encoding="utf-8")
    (tmp_path / "empty.txt").write_text("  \n", encoding="utf-8")
    (tmp_path / "ignored.txt").write_text("Não carregar.", encoding="utf-8")

    documents = TextDocumentLoader().load(tmp_path)

    assert len(documents) == 1
    assert documents[0].page_content == "Comando Linux útil."
    assert documents[0].metadata == {"source": "guide.md"}


def test_loader_raises_for_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        TextDocumentLoader().load(tmp_path / "missing")
