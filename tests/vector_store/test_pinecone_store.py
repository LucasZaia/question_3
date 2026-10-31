from semantic_search.config import Settings
from semantic_search.vector_store.pinecone_store import PineconeVectorStoreFactory


class FakePineconeClient:
    def __init__(self) -> None:
        self.created = []
        self.indexes = []

    def has_index(self, name: str) -> bool:
        return False

    def create_index(self, **kwargs) -> None:
        self.created.append(kwargs)

    def Index(self, name: str):
        self.indexes.append(name)
        return f"index:{name}"


def test_factory_creates_missing_index_with_embedding_dimension() -> None:
    client = FakePineconeClient()
    captured = {}

    def client_factory(api_key: str):
        assert api_key == "test-key"
        return client

    def vector_store_factory(**kwargs):
        captured.update(kwargs)
        return "vector-store"

    settings = Settings(
        _env_file=None,
        openai_api_key="openai-test-key",
        pinecone_api_key="test-key",
    )
    result = PineconeVectorStoreFactory(
        settings,
        embeddings="embeddings",
        client_factory=client_factory,
        vector_store_factory=vector_store_factory,
    ).create()

    assert result.vector_store == "vector-store"
    assert client.created[0]["name"] == "semantic-search-openai"
    assert client.created[0]["dimension"] == 1536
    assert client.created[0]["metric"] == "cosine"
    assert captured == {
        "index": "index:semantic-search-openai",
        "embedding": "embeddings",
        "namespace": "default",
    }
