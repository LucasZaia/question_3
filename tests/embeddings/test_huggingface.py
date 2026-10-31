from semantic_search.config import Settings
from semantic_search.embeddings.openai import OpenAIEmbeddingProvider, create_embeddings


def test_create_embeddings_uses_openai_sdk_directly(monkeypatch) -> None:
    calls = {}

    class FakeEmbeddingsApi:
        def create(self, **kwargs):
            calls["request"] = kwargs
            return type(
                "Response",
                (),
                {"data": [
                    type("Item", (), {"embedding": [0.1, 0.2]})(),
                    type("Item", (), {"embedding": [0.3, 0.4]})(),
                ]},
            )()

    class FakeOpenAI:
        def __init__(self, **kwargs):
            calls["client"] = kwargs
            self.embeddings = FakeEmbeddingsApi()

    monkeypatch.setattr("semantic_search.embeddings.openai.OpenAI", FakeOpenAI)

    settings = Settings(
        _env_file=None,
        openai_api_key="openai-test-key",
        pinecone_api_key="pinecone-test-key",
    )
    embeddings = create_embeddings(settings)

    vectors = embeddings.embed_documents(["primeiro", "segundo"])

    assert isinstance(embeddings, OpenAIEmbeddingProvider)
    assert calls["client"] == {"api_key": "openai-test-key"}
    assert calls["request"] == {
        "input": ["primeiro", "segundo"],
        "model": "text-embedding-3-small",
    }
    assert len(vectors) == 2
    assert len(vectors[0]) == 2
