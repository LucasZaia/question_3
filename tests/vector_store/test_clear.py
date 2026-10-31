from semantic_search.clear import clear_namespace
from semantic_search.config import Settings


class FakeIndex:
    def __init__(self) -> None:
        self.calls = []

    def delete(self, **kwargs) -> None:
        self.calls.append(kwargs)


class FakePineconeClient:
    def __init__(self) -> None:
        self.index = FakeIndex()

    def Index(self, name: str):
        assert name == "semantic-search-openai"
        return self.index


def test_clear_namespace_deletes_all_vectors_without_deleting_index() -> None:
    client = FakePineconeClient()
    settings = Settings(
        _env_file=None,
        openai_api_key="openai-test-key",
        pinecone_api_key="test-key",
    )

    clear_namespace(settings, client_factory=lambda api_key: client)

    assert client.index.calls == [{"delete_all": True, "namespace": "default"}]
