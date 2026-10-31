import json

from semantic_search.models import SearchResult
from semantic_search.reranking.openai_reranker import OpenAIReranker


def test_openai_reranker_reorders_candidates_from_structured_response(monkeypatch) -> None:
    calls = {}

    class FakeCompletions:
        def create(self, **kwargs):
            calls["request"] = kwargs
            return type(
                "Response",
                (),
                {
                    "choices": [
                        type(
                            "Choice",
                            (),
                            {
                                "message": type(
                                    "Message",
                                    (),
                                    {"content": json.dumps({"ranking": ["2", "1"]})},
                                )()
                            },
                        )()
                    ]
                },
            )()

    class FakeOpenAI:
        def __init__(self, **kwargs):
            self.chat = type("Chat", (), {"completions": FakeCompletions()})()

    monkeypatch.setattr("semantic_search.reranking.openai_reranker.OpenAI", FakeOpenAI)
    reranker = OpenAIReranker("test-key", "gpt-5-mini")
    candidates = [
        SearchResult(id="1", content="genérico", score=0.9, source="a.md"),
        SearchResult(id="2", content="resposta exata", score=0.8, source="b.md"),
    ]

    results = reranker.rerank("arquitetura", candidates, limit=2)

    assert [result.id for result in results] == ["2", "1"]
    assert calls["request"]["model"] == "gpt-5-mini"
    assert calls["request"]["response_format"] == {"type": "json_object"}
    assert "temperature" not in calls["request"]
